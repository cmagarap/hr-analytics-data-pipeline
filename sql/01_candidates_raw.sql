CREATE TABLE candidates (
candidate_id INT PRIMARY KEY,
full_name VARCHAR(255),
email VARCHAR(255),
phone VARCHAR(20),
address VARCHAR(255),
city VARCHAR(100),
state VARCHAR(100),
postal_code VARCHAR(20),
country VARCHAR(100)
);

INSERT INTO candidates (candidate_id, full_name, email, phone, address, city, state,
postal_code, country)
VALUES
(1, 'Alice Smith', 'alice@example.com', '555-1234', '123 Elm St', 'Sydney', 'NSW', '2000', 'Australia'),
(2, 'Bob Johnson', 'bob@example.com', '555-5678', '456 Oak St', 'Melbourne', 'VIC', '3000', 'Australia'),
(3, 'Charlie Brown', 'charlie@example.com', '555-8765', '789 Pine St', 'Brisbane', 'QLD', '4000', 'Australia'),
(4, 'David Lee', 'david@gmail', '55-02345', '321 Birch St', 'Perth', 'WA', '6000', 'Australia'),
(5, 'Emma Wilson', 'emma@', '50-006789', '654 Cedar St', 'Adelaide', 'SA', '5000', 'Australia'),
(6, 'Frank White', 'frank', '555-4321', '987 Maple St', 'Canberra', 'ACT', '2600', 'Australia');
