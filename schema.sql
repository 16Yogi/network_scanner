DROP DATABASE scan_data IF EXIST scanner

CREATE DATABASE scanner;

USE scanner;

CREATE TABLE user_registration (
    fullname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE scan_data (
    scan_device_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(255),
    device_type VARCHAR(255),
    device_ip VARCHAR(255),
    current_location VARCHAR(255),
    scan_date DATETIME
);
