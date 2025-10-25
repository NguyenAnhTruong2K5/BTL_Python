-- ========================================
-- Trigger: Giảm slot, kích hoạt thẻ khi check-in
-- ========================================
CREATE TRIGGER trg_OnInsert_ParkingRecord
ON ParkingRecord
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

        -- Giảm số chỗ trống còn lại
    -- Kiểm tra xe có hợp đồng còn hiệu lực hay không
    IF EXISTS (
        SELECT 1 FROM inserted i
        JOIN Contract c ON i.plate_number = c.plate_number
        WHERE c.end_date >= GETDATE()
    )
    BEGIN
        -- Nếu xe có hợp đồng, chỉ được gửi ở bãi A
        IF EXISTS (
            SELECT 1 FROM inserted i
            JOIN ParkingSlot ps ON ps.slot_id = i.slot_id
            WHERE ps.slot_name <> 'A'
        )
        BEGIN
            RAISERROR('Xe có hợp đồng chỉ được gửi ở bãi A.', 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
    END
    ELSE
    BEGIN
        -- Xe không có hợp đồng chỉ được gửi ở bãi B
        IF EXISTS (
            SELECT 1 FROM inserted i
            JOIN ParkingSlot ps ON ps.slot_id = i.slot_id
            WHERE ps.slot_name <> 'B'
        )
        BEGIN
            RAISERROR('Xe không có hợp đồng chỉ được gửi ở bãi B.', 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
    END

    -- Giảm slot trống
    UPDATE ps
    SET ps.slots = ps.slots - 1
    FROM ParkingSlot ps
    JOIN inserted i ON ps.slot_id = i.slot_id
    WHERE ps.slots > 0;

    -- Kích hoạt thẻ
    UPDATE c
    SET c.status = 'active', c.plate_number = i.plate_number
    FROM Card c
    JOIN inserted i ON c.card_id = i.card_id;
END;
GO

-- ========================================
-- Trigger: Check-out -> tính phí, tạo hóa đơn, tăng slot, reset thẻ
-- ========================================
CREATE TRIGGER trg_OnUpdate_ParkingRecord
ON ParkingRecord
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    ;WITH CheckoutRecords AS (
        SELECT 
            i.record_id, i.plate_number, i.card_id
        FROM inserted i
        JOIN deleted d ON i.record_id = d.record_id
        WHERE i.check_out_time IS NOT NULL AND d.check_out_time IS NULL
    )
    SELECT * INTO #tmpCheckout FROM CheckoutRecords;

    IF EXISTS (SELECT 1 FROM #tmpCheckout)
    BEGIN
        DECLARE 
            @rid VARCHAR(20),
            @plate NVARCHAR(20),
            @cid VARCHAR(20),
            @fee DECIMAL(18,2),
            @hours_total INT,
            @card_status NVARCHAR(20);

        DECLARE cur CURSOR FAST_FORWARD FOR
            SELECT record_id, plate_number, card_id FROM #tmpCheckout;

        OPEN cur;
        FETCH NEXT FROM cur INTO @rid, @plate, @cid;

        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- Kiểm tra trạng thái của thẻ trước khi checkout
            SELECT @card_status = status FROM Card WHERE card_id = @cid;
            IF @card_status <> 'active'
            BEGIN
                RAISERROR ('Không thể check-out: thẻ không active.', 16, 1);
                ROLLBACK TRANSACTION;
                RETURN;
            END

            -- Tính phí
            EXEC sp_CalcFeeForRecord @record_id = @rid,
                                     @out_fee = @fee OUTPUT,
                                     @out_hours_total = @hours_total OUTPUT;

            -- Nếu fee > 0, tạo hóa đơn
            IF @fee > 0
                EXEC sp_CreateInvoice @rid, @fee, 'cash';
            
            -- Tăng lại slot
            UPDATE ps
            SET ps.slots = ps.slots + 1
            FROM ParkingSlot ps
            JOIN ParkingRecord pr ON ps.slot_id = pr.slot_id
            WHERE pr.record_id = @rid;

            -- Cập nhật Card thành inactive và xóa dữ liệu xe
            UPDATE Card
            SET status = 'inactive', plate_number = NULL
            WHERE card_id = @cid;

            FETCH NEXT FROM cur INTO @rid, @plate, @cid;
        END

        CLOSE cur;
        DEALLOCATE cur;
    END

    DROP TABLE #tmpCheckout;
END;
GO

-- ========================================
-- Trigger: Khi tạo hoặc chỉnh sửa hợp đồng
-- Tác dụng:
--  - Tự động đặt start_date = thời điểm hiện tại
--  - Tự động tính lại end_date dựa vào term + duration
-- ========================================
CREATE TRIGGER trg_AutoUpdate_ContractDates
ON Contract
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Cập nhật start_date = thời điểm hiện tại mỗi khi thêm hoặc sửa
    UPDATE c
    SET c.start_date = GETDATE()
    FROM Contract c
    JOIN inserted i ON c.plate_number = i.plate_number;

    -- Tự động tính lại end_date dựa vào term + duration (từ thời điểm hiện tại)
    UPDATE c
    SET c.end_date = 
        CASE 
            WHEN i.term = 'monthly' THEN DATEADD(MONTH, i.duration, GETDATE())
            WHEN i.term = 'yearly'  THEN DATEADD(YEAR, i.duration, GETDATE())
        END
    FROM Contract c
    JOIN inserted i ON c.plate_number = i.plate_number;
END;
GO
