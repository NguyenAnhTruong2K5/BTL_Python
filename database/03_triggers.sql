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
        SELECT i.record_id, i.vehicle_id, i.card_id
        FROM inserted i
        JOIN deleted d ON i.record_id = d.record_id
        WHERE i.check_out_time IS NOT NULL AND d.check_out_time IS NULL
    )
    SELECT * INTO #tmpCheckout FROM CheckoutRecords;

    IF EXISTS (SELECT 1 FROM #tmpCheckout)
    BEGIN
        DECLARE @rid INT, @veh_id INT, @cid INT, @fee DECIMAL(18,2), @hours_total INT;

        DECLARE cur CURSOR FAST_FORWARD FOR
            SELECT record_id, vehicle_id, card_id FROM #tmpCheckout;

        OPEN cur;
        FETCH NEXT FROM cur INTO @rid, @veh_id, @cid;
        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- Tính phí
            EXEC sp_CalcFeeForRecord 
                @record_id = @rid, 
                @out_fee = @fee OUTPUT, 
                @out_hours_total = @hours_total OUTPUT;

            -- Nếu fee > 0, tự động tạo hóa đơn cho người check out
            IF @fee > 0
                EXEC sp_CreateInvoice @rid, @fee, 'cash';

            -- Tăng lại slot
            UPDATE ps
            SET ps.slots = ps.slots + 1
            FROM ParkingSlots ps
            JOIN ParkingRecords pr ON ps.slot_id = pr.slot_id
            WHERE pr.record_id = @rid;

            -- Cập nhật Card thành inactive và xóa dữ liệu vehicle_id (để tái sử dụng lại)
            UPDATE Cards
            SET status = 'inactive',
                vehicle_id = NULL
            WHERE card_id = @cid;

            FETCH NEXT FROM cur INTO @rid, @veh_id, @cid;
        END

        CLOSE cur;
        DEALLOCATE cur;
    END

    DROP TABLE #tmpCheckout;
END;
GO


