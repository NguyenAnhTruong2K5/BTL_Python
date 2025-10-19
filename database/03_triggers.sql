CREATE TRIGGER trg_OnInsert_ParkingRecord
ON ParkingRecords
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- Giảm số slot trống
    UPDATE ps
    SET ps.slots = ps.slots - 1
    FROM ParkingSlots ps
    JOIN inserted i ON ps.slot_id = i.slot_id
    WHERE i.check_in_time IS NOT NULL AND ps.slots > 0;

    -- Cập nhật Card thành active + gắn vehicle (thông tin xe)
    UPDATE c
    SET c.status = 'active',
        c.vehicle_id = i.vehicle_id
    FROM Cards c
    JOIN inserted i ON c.card_id = i.card_id;
END;
GO


-- ========================================
-- Trigger: check-out cập nhật fee, tăng slots khi có check out, tạo invoice, 
-- Cập nhật Card thành inactive khi check out
-- ========================================
CREATE TRIGGER trg_OnUpdate_ParkingRecord
ON ParkingRecords
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    ;WITH CheckoutRecords AS (
        SELECT 
            i.record_id,
            i.vehicle_id,
            i.card_id
        FROM inserted i
        JOIN deleted d ON i.record_id = d.record_id
        WHERE i.check_out_time IS NOT NULL 
          AND d.check_out_time IS NULL
    )
    SELECT * INTO #tmpCheckout FROM CheckoutRecords;

    IF EXISTS (SELECT 1 FROM #tmpCheckout)
    BEGIN
        DECLARE 
            @rid VARCHAR(20),
            @veh_id VARCHAR(20),
            @cid VARCHAR(20),
            @fee DECIMAL(18,2),
            @hours_total INT,
            @card_status NVARCHAR(20);

        DECLARE cur CURSOR FAST_FORWARD FOR
            SELECT record_id, vehicle_id, card_id FROM #tmpCheckout;

        OPEN cur;
        FETCH NEXT FROM cur INTO @rid, @veh_id, @cid;

        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- Kiểm tra trạng thái của thẻ trước khi checkout
            SELECT @card_status = status FROM Cards WHERE card_id = @cid;

            IF @card_status <> 'active'
            BEGIN
                RAISERROR ('Không thể check-out: thẻ này không ở trạng thái active (có thể bị rơi hoặc vô hiệu).', 16, 1);
                ROLLBACK TRANSACTION;
                RETURN;
            END

            -- Tính phí
            EXEC sp_CalcFeeForRecord 
                @record_id = @rid,
                @out_fee = @fee OUTPUT,
                @out_hours_total = @hours_total OUTPUT;

            -- Nếu fee > 0, tạo hóa đơn
            IF @fee > 0
                EXEC sp_CreateInvoice @rid, @fee, 'cash';

            -- Tăng lại slot
            UPDATE ps
            SET ps.slots = ps.slots + 1
            FROM ParkingSlots ps
            JOIN ParkingRecords pr ON ps.slot_id = pr.slot_id
            WHERE pr.record_id = @rid;

            -- Cập nhật Card thành inactive và xóa dữ liệu xe
            UPDATE Cards
            SET status = 'inactive', vehicle_id = NULL
            WHERE card_id = @cid;

            FETCH NEXT FROM cur INTO @rid, @veh_id, @cid;
        END

        CLOSE cur;
        DEALLOCATE cur;
    END

    DROP TABLE #tmpCheckout;
END;
GO

-- ========================================
-- Trigger tự động tính end_date khi thêm mới hợp đồng
-- ========================================
CREATE TRIGGER trg_CalcEndDate_OnInsertContract
ON Contracts
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
    FROM Contracts c
    JOIN inserted i ON c.vehicle_id = i.vehicle_id;
END;
GO
