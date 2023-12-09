
-- CREATE DB
CREATE DATABASE dbstore;

-- USE DB
USE dbstore;

-- CREATE TABLES
CREATE TABLE Customer (
    custID INT PRIMARY KEY AUTO_INCREMENT,
    custFname VARCHAR(255),
    custLName VARCHAR(255),
    isMember BOOLEAN
);

CREATE TABLE Item (
    itemID INT PRIMARY KEY AUTO_INCREMENT,
    itemName VARCHAR(255),
    itemQuantity INT,
    itemPrice DECIMAL(10, 2)
);

CREATE TABLE Orders (
    orderID INT PRIMARY KEY AUTO_INCREMENT,
    itemID INT,
    custID INT,
    orderQuantity INT,
    orderTotalPrice DECIMAL(10, 2),
    FOREIGN KEY (itemID) REFERENCES Item(itemID),
    FOREIGN KEY (custID) REFERENCES Customer(custID)
);


-- CREATE VIEW

CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `dbstore`.`customer_view` AS
    SELECT 
        `dbstore`.`customer`.`custID` AS `custID`,
        `dbstore`.`customer`.`custFname` AS `custFname`,
        `dbstore`.`customer`.`custLName` AS `custLName`,
        `dbstore`.`customer`.`isMember` AS `isMember`
    FROM
        `dbstore`.`customer`

CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `dbstore`.`item_view` AS
    SELECT 
        `dbstore`.`item`.`itemID` AS `itemID`,
        `dbstore`.`item`.`itemName` AS `itemName`,
        `dbstore`.`item`.`itemQuantity` AS `itemQuantity`,
        `dbstore`.`item`.`itemPrice` AS `itemPrice`
    FROM
        `dbstore`.`item`

-- CREATE STORED PROCEDURES

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_customer`(
	IN p_custFname varchar(200),
	IN p_custLname varchar(200),
	IN p_isMember boolean
)
BEGIN
    DECLARE p_custID INT;
    INSERT INTO customer (custFname, custLname, isMember)
      VALUES (p_custFname, p_custLname, p_isMember);
    SET p_custID = LAST_INSERT_ID();
    SELECT p_custID AS custID;
END

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_item`(
    IN p_itemName varchar(200),
    IN p_itemQuantity INT,
    IN p_itemPrice DECIMAL(10, 2)
)
BEGIN
    DECLARE p_itemID INT;
    INSERT INTO item (itemName, itemQuantity, itemPrice)
      VALUES (p_itemName, p_itemQuantity, p_itemPrice);
    SET p_itemID = LAST_INSERT_ID();
    SELECT p_itemID AS itemID;
END

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_customer`(
	IN p_custID INT,
	IN p_custFname varchar(200),
	IN p_custLname varchar(200),
	IN p_isMember boolean
)
BEGIN
	UPDATE customer
    SET custFname = p_custFname,
		custLname = p_custLname,
        isMember = p_isMember
	WHERE custID = p_custID;
    SELECT p_custID AS custID;
END

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_item`(
	IN p_itemID INT,
	IN p_itemName varchar(200),
	IN p_itemQuantity INT,
	IN p_itemPrice DECIMAL(10, 2)
)
BEGIN
	UPDATE item
    SET itemName = p_itemName,
		itemQuantity = p_itemQuantity,
        itemPrice = p_itemPrice
	WHERE itemID = p_itemID;
    SELECT p_itemID AS itemID;
END