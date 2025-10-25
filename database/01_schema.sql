CREATE DATABASE ParkingManagement;
GO

USE ParkingManagement;
GO

-- ========================================
-- SEQUENCES
-- ========================================
CREATE SEQUENCE seq_slot START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_card START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_record START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_invoice START WITH 1 INCREMENT BY 1;
GO

-- ========================================
-- Customers
-- ========================================
CREATE TABLE Customer (
    cccd NVARCHAR(20) PRIMARY KEY,                  
    name NVARCHAR(100) NOT NULL,
    phone_number NVARCHAR(20) NOT NULL UNIQUE,      
    email NVARCHAR(100)
);
GO

-- ========================================
-- Vehicles
-- ========================================
CREATE TABLE Vehicle (
    plate_number NVARCHAR(20) PRIMARY KEY,
    cccd NVARCHAR(20) NOT NULL,                  
    vehicle_type NVARCHAR(20) NOT NULL CHECK(vehicle_type IN ('motorbike','car')),
    FOREIGN KEY (cccd) REFERENCES Customer(cccd)
);
GO

-- ========================================
-- ParkingSlots
-- ========================================
CREATE TABLE ParkingSlot (
    slot_id VARCHAR(20) PRIMARY KEY 
        DEFAULT ('SLOT' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_slot AS VARCHAR(6)), 6)),
    slot_name NVARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    slots INT NOT NULL
);
GO

-- ========================================
-- Pricing
-- ========================================
CREATE TABLE Pricing (
    pricing_id VARCHAR(20) PRIMARY KEY,
    vehicle_type NVARCHAR(20) NOT NULL CHECK(vehicle_type IN ('motorbike','car')),
    term NVARCHAR(10) NOT NULL CHECK(term IN ('hourly','monthly','yearly')),
    rate DECIMAL(18,2) NOT NULL
);
GO

-- ========================================
-- Contracts
-- ========================================
CREATE TABLE Contract (
    plate_number NVARCHAR(20) PRIMARY KEY,           -- mỗi xe chỉ có 1 hợp đồng tại 1 thời điểm
    cccd NVARCHAR(20) NOT NULL,                      -- chủ xe
    pricing_id VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    term NVARCHAR(10) CHECK (term IN ('monthly','yearly')) NOT NULL,
    duration INT NOT NULL,
    vehicle_type NVARCHAR(20) NOT NULL CHECK(vehicle_type IN ('motorbike','car')), 
    FOREIGN KEY (pricing_id) REFERENCES Pricing(pricing_id),
    FOREIGN KEY (plate_number) REFERENCES Vehicle(plate_number),
    FOREIGN KEY (cccd) REFERENCES Customer(cccd)
);
GO

-- ========================================
-- Cards
-- ========================================
CREATE TABLE Card (
    card_id VARCHAR(20) PRIMARY KEY 
        DEFAULT ('CARD' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_card AS VARCHAR(6)), 6)),  
    card_qr NVARCHAR(255) NOT NULL UNIQUE,
    plate_number NVARCHAR(20) NULL,
    status NVARCHAR(20) CHECK (status IN ('active','inactive','lost')) DEFAULT 'inactive',
    FOREIGN KEY (plate_number) REFERENCES Vehicle(plate_number)
);
GO

-- ========================================
-- ParkingRecords
-- ========================================
CREATE TABLE ParkingRecord (
    record_id VARCHAR(20) PRIMARY KEY 
        DEFAULT ('RECO' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_record AS VARCHAR(6)), 6)),
    card_id VARCHAR(20) NOT NULL,
    slot_id VARCHAR(20) NOT NULL,
    plate_number NVARCHAR(20) NOT NULL,
    check_in_time DATETIME NOT NULL,
    check_out_time DATETIME NULL,
    hours INT NULL,
    fee DECIMAL(18,2) NULL,
    FOREIGN KEY (slot_id) REFERENCES ParkingSlot(slot_id),
    FOREIGN KEY (plate_number) REFERENCES Vehicle(plate_number),
    FOREIGN KEY (card_id) REFERENCES Card(card_id)
);
GO

-- ========================================
-- Invoices
-- ========================================
CREATE TABLE Invoice (
    invoice_id VARCHAR(20) PRIMARY KEY 
        DEFAULT ('INVO' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_invoice AS VARCHAR(6)), 6)),
    record_id VARCHAR(20) NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    method NVARCHAR(20) NULL,
    payment_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (record_id) REFERENCES ParkingRecord(record_id)
);
GO
