-- ========================================
-- Trigger: Giảm slot, kích hoạt thẻ khi check-in
-- ========================================
CREATE TRIGGER trg_OnInsert_ParkingRecord
ON ParkingRecord
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- Giảm số slot trống
    UPDATE ps
    SET ps.slots = ps.slots - 1
    FROM ParkingSlot ps
    JOIN inserted i ON ps.slot_id = i.slot_id
    WHERE i.check_in_time IS NOT NULL AND ps.slots > 0;

    -- Cập nhật Card thành active + gắn vehicle (thông tin xe)
    UPDATE c
    SET c.status = 'active',
        c.plate_number = i.plate_number
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
-- Trigger: Tự tính end_date khi tạo hợp đồng
-- ========================================
CREATE TRIGGER trg_CalcEndDate_OnInsertContract
ON Contract
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE c
    SET end_date = 
        CASE 
            WHEN i.term = 'monthly' THEN DATEADD(MONTH, i.duration, i.start_date)
            WHEN i.term = 'yearly' THEN DATEADD(YEAR, i.duration, i.start_date)
        END
    FROM Contract c
    JOIN inserted i ON c.plate_number = i.plate_number;
END;
GO
