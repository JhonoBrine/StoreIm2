
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

CREATE VIEW customer_view AS
	SELECT customer.custID, 
		customer.custFname,
        customer.custLName,
        customer.isMember
FROM customer  



CREATE VIEW customer_orders_view AS
	SELECT customer.custID, 
		customer.custFname,
        customer.custLName,
        customer.isMember,
        orders.orderID,
        item.itemName,
        orders.orderQuantity,
        orders.orderTotalPrice
FROM customer
INNER JOIN orders ON customer.custID = orders.custID
INNER JOIN item ON orders.itemID = item.itemID;



CREATE VIEW orders_view AS
	SELECT orders.orderID,
		orders.itemID,
        orders.custID,
        orders.orderQuantity,
        orders.orderTotalPrice
FROM orders; 


CREATE VIEW items_view AS
	SELECT item.itemID,
		item.itemName,
        item.itemQuantity,
        item.itemPrice
FROM item; 

-- CREATE STORED PROCEDURES

DELIMITER $$$
CREATE PROCEDURE create_customer(
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
END$$$
DELIMITER ;

DELIMITER $$$
CREATE PROCEDURE create_item(
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
END$$$
DELIMITER ;

DELIMITER $$$
CREATE PROCEDURE update_customer(
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
END$$$
DELIMITER ;


DELIMITER $$$
CREATE PROCEDURE update_item(
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
END$$$
DELIMITER ;

-- CREATE ORDER STORED PROCEDURE

DELIMITER $$$
CREATE PROCEDURE create_order(
	IN p_itemID INT,
	IN p_custID INT,
	IN p_orderQuantity INT
)
BEGIN
	DECLARE p_orderID INT;
    DECLARE p_totalPrice DECIMAL(10,2);
    DECLARE _custID INT;
    DECLARE _custIsMember BOOLEAN;
    DECLARE _itemID INT;
    DECLARE _itemQuantity INT;
    DECLARE _itemPrice DECIMAL(10,2);
    
    SELECT custID, isMember
    INTO _custID, _custIsMember
    FROM customer
    WHERE custID = p_custID;
    
    SELECT itemID, itemQuantity, itemPrice
    INTO _itemID, _itemQuantity, _itemPrice
    FROM item
    WHERE itemID = p_itemID;
    
    IF _custID IS NOT NULL AND _itemID IS NOT NULL THEN
    
    
      IF _itemQuantity >= p_orderQuantity AND _itemQuantity > 0 THEN
		IF _custIsMember IS TRUE THEN
			INSERT INTO orders(itemID, custID, orderQuantity, orderTotalPrice)
            VALUES(p_itemID, p_custID, p_orderQuantity, ((p_orderQuantity * _itemPrice) - (((p_orderQuantity * _itemPrice)*0.05)))
            );
            -- SET p_orderID = LAST_INSERT_ID();
            SELECT orderID, orderTotalPrice
            INTO p_orderID, p_totalPrice
            FROM orders
            WHERE orderID = LAST_INSERT_ID();
            
            SELECT p_orderID AS orderID, P_totalPrice AS orderTotalPrice, 'OK' AS result;
		ELSE
			INSERT INTO orders(itemID, custID, orderQuantity, orderTotalPrice)
            VALUES(p_itemID, p_custID, p_orderQuantity, (p_orderQuantity * _itemPrice)
            );
            -- SET p_orderID = LAST_INSERT_ID();
            SELECT orderID, orderTotalPrice
            INTO p_orderID, p_totalPrice
            FROM orders
            WHERE orderID = LAST_INSERT_ID();
            
            SELECT p_orderID AS orderID, p_totalPrice AS orderTotalPrice, 'OK' AS result;
        END IF;
      ELSE
		SELECT 'Quantity ordered exceeds the available stock.' AS result;
      END IF;  
        
    ELSE
	  SELECT 'Customer Id or Product Id does not exist.' AS result;
    END IF;  
END$$$
DELIMITER ;

DELIMITER $$$
CREATE PROCEDURE delete_customer(
  IN p_id INT
)
BEGIN
  DELETE FROM orders
  WHERE custID = p_id;

  DELETE FROM customer
  WHERE custID = p_id;
  
  SELECT custID FROM orders
  WHERE custID = p_id;
END$$$
DELIMITER ;

DELIMITER $$$
CREATE PROCEDURE delete_item(
  IN p_id INT
)
BEGIN
  DELETE FROM orders
  WHERE itemID = p_id;
  
  DELETE FROM item
  WHERE itemID = p_id;
  
  SELECT itemID FROM orders
  WHERE itemID = p_id;
END$$$
DELIMITER ;

DELIMITER $$$
-- BEFORE INSERT ORDERS TRIGGER

CREATE TRIGGER before_insert_orders
BEFORE INSERT ON Orders
FOR EACH ROW
BEGIN
    DECLARE available_quantity INT;

    -- Get the available quantity for the ordered item
    SELECT itemQuantity INTO available_quantity
    FROM Item
    WHERE itemID = NEW.itemID;

    -- Check if the order quantity is less than or equal to 0
    IF NEW.orderQuantity <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Order quantity must be greater than 0';
    -- Check if the order quantity is greater than the available quantity
    ELSEIF NEW.orderQuantity > available_quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot order more than available quantity';
    ELSE
        -- Reduce the item quantity in the Item table
        UPDATE Item
        SET itemQuantity = itemQuantity - NEW.orderQuantity
        WHERE itemID = NEW.itemID;
    END IF;
END $$$

DELIMITER ;