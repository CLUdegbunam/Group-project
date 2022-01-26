CREATE DATABASE Group5DB;

CREATE TABLE Initial_Order_Table (
    ID INT NOT NULL SMALLSERIAL PRIMARY KEY,
    Date DATE(YYYY-MM-DD) NOT NULL,
    Time TIME(hh:mm:ss) NOT NULL,
    Branch VARCHAR(255),
    Item_price FLOAT(53),
    Total_price FLOAT(53),
    Payment_Method VARCHAR(255)
);

CREATE TABLE Item (
    Item_ID INT NOT NULL SMALLSERIAL PRIMARY KEY,
    Item_Name VARCHAR(255) NOT NULL,
    Price FLOAT(53) NOT NULL
);

CREATE TABLE Order (
    Order_ID INT NOT NULL,
    Date DATE(YYYY-MM-DD) NOT NULL,
    Time TIME (hh:mm:ss) NOT NULL,
    Branch_ID INT(255) NOT NULL,
    Total_price FLOAT(53) NOT NULL,
    PRIMARY KEY (Order_ID, Branch_ID)
);

CREATE TABLE Branch (
    Branch_ID INT NOT NULL SMALLSERIAL PRIMARY KEY,
    Branch VARCHAR(255) NOT NULL
);

CREATE TABLE Items_Ordered (
    Order_ID INT NOT NULL,
    Item_ID INT(255) NOT NULL,
    Quantity INT(20) NOT NULL,
    PRIMARY KEY (Order_ID, Item_ID)
);

CREATE TABLE Customer (
    Customer_ID INT NOT NULL Smallcereal PRIMARY KEY,
    Full_Name VARCHAR(255) NOT NULL
);