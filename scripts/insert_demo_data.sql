INSERT INTO products (name, category, price) VALUES
('Laptop', 'Electronics', 999.99),
('Smartphone', 'Electronics', 699.99),
('Running Shoes', 'Fashion', 89.99),
('Bluetooth Speaker', 'Electronics', 149.99),
('Backpack', 'Fashion', 39.99);

INSERT INTO inventory (product_id, stock_level) VALUES
(1, 10),
(2, 5),
(3, 2),
(4, 20),
(5, 8);

INSERT INTO sales (product_id, quantity, total_amount, sale_date) VALUES
(1, 1, 999.99, '2024-05-10'),
(2, 2, 1399.98, '2024-05-12'),
(3, 1, 89.99, '2024-05-15'),
(1, 1, 999.99, '2024-05-16'),
(5, 3, 119.97, '2024-05-17');
