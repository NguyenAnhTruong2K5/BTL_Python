-- ========================================
-- Trigger: trg_OnUpdate_ParkingRecord
--  - Khi update ParkingRecord và check_out_time từ NULL -> NOT NULL (checkout):
--      * Gọi sp_CalcFeeForRecord để tính fee
--      * Nếu fee > 0 -> tạo bản ghi parking_invoice
--      * Tăng lại slots (bãi có slots tăng 1)
--      * Reset thẻ (status = 'inactive', plate_number = NULL)
-- ========================================
CREATE TRIGGER trg_OnUpdate_ParkingRecord
ON ParkingRecord
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    ;WITH CheckoutRecords AS (
        SELECT i.record_id, i.plate_number, i.card_id
        FROM inserted i
        JOIN deleted d ON i.record_id = d.record_id
        WHERE i.check_out_time IS NOT NULL AND d.check_out_time IS NULL
    )
    SELECT * INTO #tmpCheckout FROM CheckoutRecords;

    IF EXISTS (SELECT 1 FROM #tmpCheckout)
    BEGIN
        DECLARE @rid VARCHAR(20), @plate NVARCHAR(20), @cid VARCHAR(20);
        DECLARE @fee DECIMAL(18,2);
        DECLARE @pricing_id VARCHAR(50);

        DECLARE cur CURSOR LOCAL FAST_FORWARD FOR
            SELECT record_id, plate_number, card_id FROM #tmpCheckout;

        OPEN cur;
        FETCH NEXT FROM cur INTO @rid, @plate, @cid;
        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- Kiểm tra thẻ active
            IF NOT EXISTS (SELECT 1 FROM Card WHERE card_id = @cid AND status = 'active')
            BEGIN
                RAISERROR('Không thể check-out: thẻ không active.', 16, 1);
                ROLLBACK TRANSACTION;
                RETURN;
            END

            -- Tính phí
            SET @fee = 0;
            EXEC sp_CalcFeeForRecord @record_id = @rid, @out_fee = @fee OUTPUT;

            -- Nếu có phí > 0 tạo parking_invoice
            IF @fee > 0
            BEGIN
                -- Lấy pricing_id theo vehicle_type đã lưu trong ParkingRecord (nếu muốn lưu loại áp dụng)
                SELECT TOP 1 @pricing_id = p.pricing_id
                FROM Pricing p
                JOIN ParkingRecord pr ON pr.record_id = @rid
                WHERE p.vehicle_type = pr.vehicle_type AND p.term = 'hourly';

                EXEC sp_CreateParkingInvoice @record_id = @rid, @pricing_id = @pricing_id, @amount = @fee, @method = 'cash';
            END

            -- Tăng lại slots 
            UPDATE ParkingSlot SET slots = slots + 1;

            -- Reset thẻ
            UPDATE Card
            SET status = 'inactive',
                plate_number = NULL
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
-- Trigger: trg_AutoUpdate_ContractDates
--  - Khi INSERT hoặc UPDATE Contract:
--      * Tự đặt start_date = NOW()
--      * Tính end_date dựa trên term + duration (month/year)
--      * (Không tự động giảm slots — theo yêu cầu: "không còn insert contract nữa" / slot không bị trừ khi tạo contract)
-- ========================================
CREATE TRIGGER trg_AutoUpdate_ContractDates
ON Contract
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Đặt start_date = thời điểm hiện tại mỗi khi thêm hoặc sửa
    UPDATE c
    SET c.start_date = CAST(GETDATE() AS DATE)
    FROM Contract c
    JOIN inserted i ON c.plate_number = i.plate_number;

    -- Tự tính end_date từ start_date (hiện tại là thời điểm GETDATE())
    UPDATE c
    SET c.end_date =
        CASE
            WHEN i.term = 'monthly' THEN DATEADD(MONTH, i.duration, CAST(GETDATE() AS DATE))
            WHEN i.term = 'yearly'  THEN DATEADD(YEAR, i.duration, CAST(GETDATE() AS DATE))
        END
    FROM Contract c
    JOIN inserted i ON c.plate_number = i.plate_number;
END;
GO
