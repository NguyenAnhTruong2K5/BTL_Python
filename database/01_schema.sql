-- ========================================
-- Tạo database
-- ========================================
CREATE DATABASE ParkingManagement;
GO

USE ParkingManagement;
GO
    
-- ========================================
-- Tạo SEQUENCE cho các bảng có mã tự tăng định dạng
-- ========================================
CREATE SEQUENCE seq_customer START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_vehicle START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_slot START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_contract START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_card START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_record START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_invoice START WITH 1 INCREMENT BY 1;
GO

-- ========================================
-- Bảng Customers
-- ========================================
CREATE TABLE Customers (
    customer_id VARCHAR(20) PRIMARY KEY 
        DEFAULT ('cusid' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_customer AS VARCHAR(6)), 6)),
    name NVARCHAR(100),
    phone_number NVARCHAR(20),
    email NVARCHAR(100)
);
GO

-- ========================================
-- Bảng Vehicle
-- ========================================
CREATE TABLE Vehicle (
    vehicle_id VARCHAR(20) PRIMARY KEY 
        DEFAULT ('vehid' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_vehicle AS VARCHAR(6)), 6)),
    customer_id INT NOT NULL,
    vehicle_type NVARCHAR(20) NOT NULL CHECK(vehicle_type IN ('motorbike','car')),
    plate_number NVARCHAR(20) UNIQUE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);
GO

-- ========================================
-- Bảng ParkingSlots
-- ========================================
CREATE TABLE ParkingSlots (
    slot_id VARCHAR(20) PRIMARY KEY 
        DEFAULT ('slotid' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_slot AS VARCHAR(6)), 6)),
    slot_name NVARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    slots INT NOT NULL
);
GO

-- ========================================
-- Bảng Pricing
-- ========================================
CREATE TABLE Pricing (
    pricing_id VARCHAR(20) PRIMARY KEY,
    vehicle_type NVARCHAR(20) NOT NULL CHECK(vehicle_type IN ('motorbike','car')),
    type NVARCHAR(20) NOT NULL CHECK(type IN ('hourly','monthly')),
    rate DECIMAL(18,2) NOT NULL
);
GO

-- ========================================
-- Bảng Contracts (monthly)
-- ========================================
CREATE TABLE Contracts (
    vehicle_id INT PRIMARY KEY,      -- vehicle là khóa chính
    pricing_id INT NOT NULL,
    customer_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,              -- sẽ được tự động tính: start_date + thời gian hợp đồng (bao tháng, bao năm)
    duration_type NVARCHAR(10) CHECK (duration_type IN ('month','year')) NOT NULL,    -- loại thời hạn (tháng/năm)
    duration_value INT NOT NULL,     -- số tháng hoặc năm
    FOREIGN KEY (pricing_id) REFERENCES Pricing(pricing_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);
GO

-- ========================================
-- Bảng Cards
-- ========================================
CREATE TABLE Cards (
    card_id VARCHAR(20) PRIMARY KEY 
        DEFAULT ('cardid' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_card AS VARCHAR(6)), 6)),  
    card_qr NVARCHAR(255) NOT NULL UNIQUE,      -- Chuỗi QR (unique)
    vehicle_id INT NULL,                    -- Gắn với 1 xe
    status NVARCHAR(20) CHECK (status IN ('active','inactive','lost')) DEFAULT 'inactive',
    -- active (có người sử dụng), inactive (chưa có người sử dụng), lost (mất thẻ, admin phải tự cập nhật)
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id)
);
GO

-- ========================================
-- Bảng ParkingRecords
-- ========================================
CREATE TABLE ParkingRecords (
    record_id VARCHAR(20) PRIMARY KEY 
        DEFAULT ('recid' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_record AS VARCHAR(6)), 6)),
    card_id INT NOT NULL,
    slot_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    check_in_time DATETIME NOT NULL,
    check_out_time DATETIME NULL,
    hours INT NULL,
    fee DECIMAL(18,2) NULL,
    FOREIGN KEY (slot_id) REFERENCES ParkingSlots(slot_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id),
    FOREIGN KEY (card_id) REFERENCES Cards(card_id)
);
GO

-- ========================================
-- Bảng Invoices
-- ========================================
CREATE TABLE Invoices (
    invoice_id VARCHAR(20) PRIMARY KEY 
        DEFAULT ('invid' + RIGHT('000000' + CAST(NEXT VALUE FOR seq_invoice AS VARCHAR(6)), 6)),
    record_id INT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    method NVARCHAR(20) NULL,
    payment_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (record_id) REFERENCES ParkingRecords(record_id)
);
GO

