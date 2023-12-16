from database import fetchall, fetchone, execute

### CREATE Order

def create_order(data):
    cur = execute("""CALL create_order(%s, %s, %s)""", (data["itemID"], data["custID"], data["orderQuantity"]))
    row = cur.fetchone()
    
    try:
        data["orderID"] = row["orderID"]
        data["orderTotalPrice"] = row["orderTotalPrice"]
        data["result"] = row["result"]
        
        return data
    except KeyError as e:
        return ("Order cannot be made due to Item or Customer not existing")
    
    


    

### Read all Order List

def get_all_orders():
    cur = fetchall("""SELECT * FROM orders_view""")
    return cur

### Read Single Order

def get_order_by_id(id):
    cur = fetchone("""SELECT * FROM orders_view WHERE orderID = %s""", (id,))
    return cur

### Update Single Order

def update_order(id,data):
    result = None
    row = result.fetchone()
    
    data["orderID"] = row["orderID"]
    
    return data

### Delete Single Order

def delete_order(id):
    
    result = execute("""DELETE FROM orders WHERE orderID = %s""", (id,))
    result.fetchone()
    
    return result.rowcount > 0