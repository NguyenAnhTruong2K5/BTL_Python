-- ========================================
-- Trigger: trg_OnInsert_ParkingRecord
-- ========================================
CREATE TRIGGER trg_OnInsert_ParkingRecord
ON ParkingRecord
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @current_open INT;
    SELECT @current_open = COUNT(*) FROM ParkingRecord WHERE check_out_time IS NULL;

    DECLARE @capacity INT, @slots INT;
    SELECT TOP 1 @capacity = capacity, @slots = slots FROM ParkingSlot;

    IF @slots <= 0
    BEGIN
        RAISERROR('Bãi đã đầy, không thể check-in.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    UPDATE ParkingSlot
    SET slots = slots - 1;

    UPDATE c
    SET c.status = 'active'
    FROM Card c
    JOIN inserted i ON c.card_id = i.card_id;
END;
GO

-- ========================================
-- Trigger: trg_OnUpdate_ParkingRecord
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
        DECLARE @rid VARCHAR(20), @plate VARCHAR(20), @cid VARCHAR(20);
        DECLARE @fee DECIMAL(18,2);
        DECLARE @pricing_id VARCHAR(50);

        DECLARE cur CURSOR LOCAL FAST_FORWARD FOR
            SELECT record_id, plate_number, card_id FROM #tmpCheckout;

        OPEN cur;
        FETCH NEXT FROM cur INTO @rid, @plate, @cid;
        WHILE @@FETCH_STATUS = 0
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM Card WHERE card_id = @cid AND status = 'active')
            BEGIN
                RAISERROR('Không thể check-out: thẻ không active.', 16, 1);
                ROLLBACK TRANSACTION;
                RETURN;
            END

            SET @fee = 0;
            EXEC sp_CalcFeeForRecord @record_id = @rid, @out_fee = @fee OUTPUT;

            IF @fee > 0
            BEGIN
                SELECT TOP 1 @pricing_id = p.pricing_id
                FROM Pricing p
                JOIN ParkingRecord pr ON pr.record_id = @rid
                WHERE p.vehicle_type = pr.vehicle_type AND p.term = 'hourly';

                EXEC sp_CreateParkingInvoice @record_id = @rid, @pricing_id = @pricing_id, @amount = @fee, @method = 'cash';
            END

            UPDATE ParkingSlot SET slots = slots + 1;

            UPDATE Card
            SET status = 'inactive'
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
-- ========================================
CREATE TRIGGER trg_AutoUpdate_ContractDates
ON Contract
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE c
    SET c.start_date = CAST(GETDATE() AS DATE)
    FROM Contract c
    JOIN inserted i ON c.plate_number = i.plate_number;

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
