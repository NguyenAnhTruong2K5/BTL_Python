-- ========================================
-- DỮ LIỆU MẪU
-- ========================================

-- Bảng Pricing: 4 loại giá
INSERT INTO Pricing (pricing_id, vehicle_type, type, rate)
VALUES
(1, 'motorbike', 'hourly', 3000),   -- 3k/h
(2, 'car', 'hourly', 10000),        -- 10k/h
(3, 'motorbike', 'monthly', 300000),-- 300k/tháng
(4, 'car', 'monthly', 1000000);     -- 1000k/tháng
GO

-- Bảng ParkingSlots: 3 bãi A, B, C mỗi bãi 100 chỗ
INSERT INTO ParkingSlots (slot_name, capacity, slots)
VALUES
('A', 100, 100),
('B', 100, 100),
('C', 100, 100);
GO

