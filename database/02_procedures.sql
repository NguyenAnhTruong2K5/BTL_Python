-- ========================================
-- Stored Procedure: sp_CalcFeeForRecord
--  - Tính phí cho 1 ParkingRecord (theo record_id)
--  - Quy tắc:
--      * Nếu có hợp đồng cho plate (Contract.end_date >= check_in_time):
--           - nếu check_out <= end_date => fee = 0
--           - nếu check_in < end_date < check_out => fee tính từ end_date -> check_out
--      * Nếu không có hợp đồng => tính full giờ giữa in/out
--  - Kết quả: cập nhật ParkingRecord.check_out_time (đã có), trả về @out_fee
-- ========================================
CREATE PROCEDURE sp_CalcFeeForRecord
    @record_id VARCHAR(20),
    @out_fee DECIMAL(18,2) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @in_dt DATETIME, @out_dt DATETIME, @plate VARCHAR(20), @veh_type VARCHAR(20);
    DECLARE @contract_end DATETIME = NULL;
    DECLARE @charge_minutes INT;
    DECLARE @rate DECIMAL(18,2);

    SELECT @in_dt = pr.check_in_time,
           @out_dt = pr.check_out_time,
           @plate = pr.plate_number,
           @veh_type = pr.vehicle_type
    FROM ParkingRecord pr
    WHERE pr.record_id = @record_id;

    IF @in_dt IS NULL OR @out_dt IS NULL
    BEGIN
        SET @out_fee = 0;
        RETURN;
    END

    SELECT @contract_end = end_date
    FROM Contract
    WHERE plate_number = @plate AND end_date >= @in_dt;

    IF @contract_end IS NULL
    BEGIN
        SET @charge_minutes = DATEDIFF(MINUTE, @in_dt, @out_dt);
    END
    ELSE
    BEGIN
        IF @out_dt <= @contract_end
            SET @charge_minutes = 0;
        ELSE IF @in_dt >= @contract_end
            SET @charge_minutes = DATEDIFF(MINUTE, @in_dt, @out_dt);
        ELSE
            SET @charge_minutes = DATEDIFF(MINUTE, @contract_end, @out_dt);
    END

    DECLARE @hours_chargeable INT = CEILING(CAST(ISNULL(@charge_minutes,0) AS FLOAT) / 60.0);

    SELECT TOP 1 @rate = rate FROM Pricing WHERE vehicle_type = @veh_type AND term = 'hourly';

    IF @rate IS NULL SET @rate = 0;

    SET @out_fee = @hours_chargeable * @rate;
END;
GO

-- ========================================
-- Stored Procedure: sp_CreateParkingInvoice
--   tạo bản ghi hóa đơn cho lượt đỗ (parking_invoice)
-- ========================================
CREATE PROCEDURE sp_CreateParkingInvoice
    @record_id VARCHAR(20),
    @pricing_id VARCHAR(50) = NULL,
    @amount DECIMAL(18,2),
    @method NVARCHAR(20) = 'cash'
AS
BEGIN
    SET NOCOUNT ON;
    IF @amount <= 0 RETURN; -- không tạo nếu amount <= 0

    INSERT INTO parking_invoice (record_id, pricing_id, amount, payment_date)
    VALUES (@record_id, @pricing_id, @amount, GETDATE());
END;
GO
