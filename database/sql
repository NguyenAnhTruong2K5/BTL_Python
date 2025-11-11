-- ========================================
-- Database
-- ========================================
CREATE DATABASE ParkingManagement;
GO

USE ParkingManagement;
GO

-- ========================================
-- SEQUENCES
-- ========================================
CREATE SEQUENCE seq_card START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_record START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_contract_invoice START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_parking_invoice START WITH 1 INCREMENT BY 1;
GO

-- ========================================
-- Customers
-- ========================================
CREATE TABLE Customer (
    cccd VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100)
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
    vehicle_type VARCHAR(20) NOT NULL CHECK(vehicle_type IN ('motorbike','car')),
    term VARCHAR(10) NOT NULL CHECK(term IN ('hourly','monthly','yearly')),
    rate DECIMAL(18,2) NOT NULL
);
GO

-- ========================================
-- Contract
-- ========================================
CREATE TABLE Contract (
    plate_number VARCHAR(20) PRIMARY KEY,
    cccd VARCHAR(20) NOT NULL,
    pricing_id VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    term VARCHAR(10) CHECK(term IN ('monthly','yearly')) NOT NULL,
    duration INT NOT NULL,
    vehicle_type VARCHAR(20) NOT NULL CHECK(vehicle_type IN ('motorbike','car')),
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
    card_qr VARCHAR(255) NOT NULL UNIQUE,
    status VARCHAR(20) CHECK(status IN ('active','inactive','lost')) DEFAULT 'inactive'
);
GO

-- ========================================
-- ParkingRecord
-- ========================================
CREATE TABLE ParkingRecord (
    record_id VARCHAR(20) PRIMARY KEY
        DEFAULT ('RECO' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_record AS VARCHAR(6)), 6)),
    card_id VARCHAR(20) NOT NULL,
    slot_name VARCHAR(50) NOT NULL,
    plate_number VARCHAR(20) NOT NULL,
    vehicle_type VARCHAR(20) NOT NULL CHECK(vehicle_type IN ('motorbike','car')),
    check_in_time DATETIME NOT NULL,
    check_out_time DATETIME NULL,
    image_path VARCHAR(500) NULL DEFAULT NULL,
    FOREIGN KEY (card_id) REFERENCES Card(card_id),
    FOREIGN KEY (plate_number) REFERENCES Contract(plate_number)
);
GO

-- ========================================
-- contract_invoice
-- ========================================
CREATE TABLE contract_invoice (
    invoice_id VARCHAR(30) PRIMARY KEY
        DEFAULT ('CINV' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_contract_invoice AS VARCHAR(6)), 6)),
    plate_number VARCHAR(20) NOT NULL,
    pricing_id VARCHAR(50) NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    payment_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (plate_number) REFERENCES Contract(plate_number),
    FOREIGN KEY (pricing_id) REFERENCES Pricing(pricing_id)
);
GO

-- ========================================
-- parking_invoice
-- ========================================
CREATE TABLE parking_invoice (
    invoice_id VARCHAR(30) PRIMARY KEY
        DEFAULT ('PINV' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_parking_invoice AS VARCHAR(6)), 6)),
    record_id VARCHAR(30) NOT NULL,
    plate_number VARCHAR(20) NOT NULL,
    pricing_id VARCHAR(50) NULL,
    amount DECIMAL(18,2) NOT NULL,
    payment_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (record_id) REFERENCES ParkingRecord(record_id),
    FOREIGN KEY (plate_number) REFERENCES Contract(plate_number),
    FOREIGN KEY (pricing_id) REFERENCES Pricing(pricing_id)
);
GO


    
Use ParkingManagement;
GO

INSERT INTO Pricing (pricing_id, vehicle_type, term, rate)
VALUES
('1', 'motorbike', 'hourly', 3000),   -- 3k/h
('2', 'car', 'hourly', 10000),        -- 10k/h
('3', 'motorbike', 'monthly', 300000),-- 300k/tháng
('4', 'car', 'monthly', 1000000),     -- 1000k/tháng
('5', 'motorbike', 'yearly', 800000), --800k/năm
('6', 'car', 'yearly', 2000000); --2000k/năm
GO

-- Khởi tạo duy nhất 1 dòng cho bãi A, 100 chỗ
INSERT INTO ParkingSlot (capacity, slots) VALUES (100, 100);
GO

