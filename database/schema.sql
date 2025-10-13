-- ========================================
-- Tạo database
-- ========================================
CREATE DATABASE ParkingManagement;
GO

USE ParkingManagement;
GO

-- ========================================
-- Bảng Customers
-- ========================================
CREATE TABLE Customers (
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100),
    phone_number NVARCHAR(20),
    email NVARCHAR(100)
);
GO

-- ========================================
-- Bảng Vehicle
-- ========================================
CREATE TABLE Vehicle (
    vehicle_id INT IDENTITY(1,1) PRIMARY KEY,
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
    slot_id INT IDENTITY(1,1) PRIMARY KEY,
    slot_name NVARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    slots INT NOT NULL
);
GO

-- ========================================
-- Bảng Pricing
-- ========================================
CREATE TABLE Pricing (
    pricing_id INT IDENTITY(1,1) PRIMARY KEY,
    vehicle_type NVARCHAR(20) NOT NULL CHECK(vehicle_type IN ('motorbike','car')),
    type NVARCHAR(20) NOT NULL CHECK(type IN ('hourly','monthly')),
    rate DECIMAL(18,2) NOT NULL
);
GO

-- ========================================
-- Bảng Contracts (monthly)
-- ========================================
CREATE TABLE Contracts (
    contract_id INT IDENTITY(1,1) PRIMARY KEY,
    pricing_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    customer_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (pricing_id) REFERENCES Pricing(pricing_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);
GO

-- ========================================
-- Bảng Cards
-- ========================================
CREATE TABLE Cards (
    card_id INT IDENTITY(1,1) PRIMARY KEY,      
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
    record_id INT IDENTITY(1,1) PRIMARY KEY,
    card_id INT NOT NULL,
    slot_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    check_in_time DATETIME NOT NULL,
    check_out_time DATETIME NULL,
    hours INT NULL,
    fee DECIMAL(18,2) NULL,
    FOREIGN KEY (slot_id) REFERENCES ParkingSlots(slot_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id),
    FOREIGN KEY (card_id) REFERENCES Cards(card_id);
);
GO

-- ========================================
-- Bảng Invoices
-- ========================================
CREATE TABLE Invoices (
    invoice_id INT IDENTITY(1,1) PRIMARY KEY,
    record_id INT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    method NVARCHAR(20) NULL,
    payment_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (record_id) REFERENCES ParkingRecords(record_id)
);
GO

