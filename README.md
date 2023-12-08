# StoreIm2

This repository is for the subject, CSIT327 - Information Management 2.

**Currently in the works**

# Idea

Store Prices by **Steemp**

Entities with their assigned columns
> **Customer** : [_custID{PK}_, _custFname_, _custLName_,_isMember{Boolean}_]
> **Item** : [_itemID{PK}_, _itemName_, _itemQuantity_, _itemPrice_]
> **Order** : [_orderID{PK}_, _itemID{FK}_, _custID{FK}_, _orderQuantity_, _orderTotalPrice_]

Guide (Not Final)
> Customer can order many items
> If Customer is Member, Customer can have 5% discount on items the customer bought
> ??
