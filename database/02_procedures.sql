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

    DECLARE @in_dt DATETIME, @out_dt DATETIME, @plate NVARCHAR(20), @veh_type NVARCHAR(20);
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

    -- Lấy hợp đồng (nếu có) cho plate và còn hiệu lực (end_date >= in_dt)
    SELECT TOP 1 @contract_end = DATEADD(SECOND, 86399, end_date)
    FROM Contract
    WHERE plate_number = @plate AND end_date >= @in_dt
    ORDER BY end_date DESC;

    IF @contract_end IS NULL
    BEGIN
        -- Không có hợp đồng -> tính toàn bộ thời gian giữa in/out
        SET @charge_minutes = DATEDIFF(MINUTE, @in_dt, @out_dt);
    END
    ELSE
    BEGIN
        -- Có hợp đồng
        IF @out_dt <= @contract_end
        BEGIN
            SET @charge_minutes = 0; -- nằm trong hợp đồng hoàn toàn
        END
        ELSE IF @in_dt >= @contract_end
        BEGIN
            -- Toàn bộ nằm sau khi hợp đồng hết hạn
            SET @charge_minutes = DATEDIFF(MINUTE, @in_dt, @out_dt);
        END
        ELSE
        BEGIN
            -- Một phần trước hợp đồng kết thúc (miễn phí), phần sau tính tiền
            SET @charge_minutes = DATEDIFF(MINUTE, @contract_end, @out_dt);
        END
    END

    -- Làm tròn lên giờ
    DECLARE @hours_chargeable INT = CEILING(CAST(ISNULL(@charge_minutes,0) AS FLOAT) / 60.0);

    -- Lấy đơn giá hourly theo vehicle_type (ưu tiên tìm hourly)
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
