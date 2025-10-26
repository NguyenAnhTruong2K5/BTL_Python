-- ========================================
-- Database
-- ========================================
CREATE DATABASE ParkingManagement;
GO

USE ParkingManagement;
GO

-- ========================================
-- SEQUENCES (dùng cho id tự sinh)
-- ========================================
CREATE SEQUENCE seq_card START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_record START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_contract_invoice START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_parking_invoice START WITH 1 INCREMENT BY 1;
GO

-- ========================================
-- Customer
-- ========================================
CREATE TABLE Customer (
    cccd NVARCHAR(20) PRIMARY KEY,                  
    name NVARCHAR(100) NOT NULL,
    phone_number NVARCHAR(20) NOT NULL UNIQUE,
    email NVARCHAR(100)
);
GO

-- ========================================
-- ParkingSlot
-- ========================================
CREATE TABLE ParkingSlot (
    capacity INT NOT NULL,
    slots INT NOT NULL
);
GO

-- ========================================
-- Pricing
-- ========================================
CREATE TABLE Pricing (
    pricing_id VARCHAR(50) PRIMARY KEY,
    vehicle_type NVARCHAR(20) NOT NULL CHECK(vehicle_type IN ('motorbike','car')),
    term NVARCHAR(10) NOT NULL CHECK(term IN ('hourly','monthly','yearly')),
    rate DECIMAL(18,2) NOT NULL
);
GO

-- ========================================
-- Contract
-- ========================================
CREATE TABLE Contract (
    plate_number NVARCHAR(20) PRIMARY KEY,   -- mỗi xe có tối đa 1 hợp đồng (theo plate)
    cccd NVARCHAR(20) NOT NULL,              -- chủ xe (tham chiếu Customer)
    pricing_id VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    term NVARCHAR(10) CHECK(term IN ('monthly','yearly')) NOT NULL,
    duration INT NOT NULL,                   -- số tháng hoặc số năm (tùy term)
    vehicle_type NVARCHAR(20) NOT NULL CHECK(vehicle_type IN ('motorbike','car')),
    FOREIGN KEY (cccd) REFERENCES Customer(cccd),
    FOREIGN KEY (pricing_id) REFERENCES Pricing(pricing_id)
);
GO

-- ========================================
-- Cards
-- ========================================
CREATE TABLE Card (
    card_id VARCHAR(20) PRIMARY KEY
        DEFAULT ('CARD' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_card AS VARCHAR(6)), 6)),
    card_qr NVARCHAR(255) NOT NULL UNIQUE,
    plate_number NVARCHAR(20) NULL,     -- gán tạm biển khi dùng thẻ
    status NVARCHAR(20) CHECK(status IN ('active','inactive','lost')) DEFAULT 'inactive'
    -- không có FK vì không có bảng Vehicle
);
GO

-- ========================================
-- ParkingRecord
-- ========================================
CREATE TABLE ParkingRecord (
    record_id VARCHAR(20) PRIMARY KEY
        DEFAULT ('RECO' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_record AS VARCHAR(6)), 6)),
    card_id VARCHAR(20) NOT NULL,
    slot_name NVARCHAR(50) NOT NULL,     -- tên bãi dùng: 'A' hoặc 'B' (dự án đơn bãi A nhưng giữ trường cho linh hoạt)
    plate_number NVARCHAR(20) NOT NULL,
    vehicle_type NVARCHAR(20) NOT NULL CHECK(vehicle_type IN ('motorbike','car')), -- lưu tạm
    check_in_time DATETIME NOT NULL,
    check_out_time DATETIME NULL,
    image_path NVARCHAR(500) NULL DEFAULT NULL,
    ai_plate_number NVARCHAR(50) NULL DEFAULT NULL,
    FOREIGN KEY (card_id) REFERENCES Card(card_id)
);
GO

-- ========================================
-- contract_invoice: hóa đơn khi KH mua hợp đồng (chỉ dùng cho hợp đồng)
-- ========================================
CREATE TABLE contract_invoice (
    invoice_id VARCHAR(30) PRIMARY KEY
        DEFAULT ('CINV' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_contract_invoice AS VARCHAR(6)), 6)),
    pricing_id VARCHAR(50) NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    payment_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (pricing_id) REFERENCES Pricing(pricing_id)
);
GO

-- ========================================
-- parking_invoice: hóa đơn cho từng lượt đỗ xe
-- ========================================
CREATE TABLE parking_invoice (
    invoice_id VARCHAR(30) PRIMARY KEY
        DEFAULT ('PINV' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_parking_invoice AS VARCHAR(6)), 6)),
    record_id VARCHAR(30) NOT NULL,
    pricing_id VARCHAR(50) NULL, -- có thể NULL nếu không tra được pricing
    amount DECIMAL(18,2) NOT NULL,
    payment_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (record_id) REFERENCES ParkingRecord(record_id),
    FOREIGN KEY (pricing_id) REFERENCES Pricing(pricing_id)
);
GO
