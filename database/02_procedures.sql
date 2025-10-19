-- ========================================
-- Stored Procedure tính fee
-- ========================================
CREATE PROCEDURE sp_CalcFeeForRecord
    @record_id VARCHAR(20),
    @out_fee DECIMAL(18,2) OUTPUT,
    @out_hours_total INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @in_dt DATETIME, @out_dt DATETIME, @veh_id INT, @veh_type NVARCHAR(20);
    DECLARE @contract_end DATETIME = NULL;

    SELECT @in_dt = pr.check_in_time, @out_dt = pr.check_out_time, @veh_id = pr.vehicle_id
    FROM ParkingRecords pr
    WHERE pr.record_id = @record_id;

    IF @in_dt IS NULL OR @out_dt IS NULL
    BEGIN
        SET @out_fee = 0; SET @out_hours_total = 0;
        RETURN;
    END

    SELECT @veh_type = vehicle_type FROM Vehicle WHERE vehicle_id = @veh_id;

    -- Lấy hợp đồng active mới nhất
    SELECT TOP 1 @contract_end = DATEADD(SECOND, 86399, end_date)
    FROM Contracts
    WHERE vehicle_id = @veh_id AND end_date >= @in_dt
    ORDER BY end_date DESC;

    DECLARE @charge_minutes INT;

    IF @contract_end IS NULL OR @in_dt > @contract_end
        SET @charge_minutes = DATEDIFF(MINUTE, @in_dt, @out_dt);
    ELSE IF @out_dt <= @contract_end
        SET @charge_minutes = 0;
    ELSE
        SET @charge_minutes = DATEDIFF(MINUTE, @contract_end, @out_dt);

    DECLARE @hours_total INT = CEILING(CAST(DATEDIFF(MINUTE, @in_dt, @out_dt) AS FLOAT)/60.0);
    DECLARE @hours_chargeable INT = CEILING(CAST(ISNULL(@charge_minutes,0) AS FLOAT)/60.0);

    DECLARE @rate DECIMAL(18,2) = (
        SELECT TOP 1 rate FROM Pricing
        WHERE vehicle_type = @veh_type AND term='hourly'
    );

    DECLARE @fee DECIMAL(18,2) = @hours_chargeable * ISNULL(@rate,0);

    UPDATE ParkingRecords
    SET hours = @hours_total, fee = @fee
    WHERE record_id = @record_id;

    SET @out_fee = @fee;
    SET @out_hours_total = @hours_total;
END;
GO

-- ========================================
-- Stored Procedure tạo invoice
-- ========================================
CREATE PROCEDURE sp_CreateInvoice
    @record_id VARCHAR(20),
    @amount DECIMAL(18,2),
    @method NVARCHAR(20) = 'cash'
AS
BEGIN
    SET NOCOUNT ON;

    IF @amount <= 0 RETURN;

    INSERT INTO Invoices (record_id, amount, method, payment_date)
    VALUES (@record_id, @amount, @method, GETDATE());
END;
GO

