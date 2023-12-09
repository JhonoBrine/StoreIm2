from database import fetchall, fetchone, execute

### CREATE Order

def create_order(data):
    result = None
    row = result.fetchone()
    
    data["orderID"] = row["orderID"]
    
    return data

### Read all Order List

def get_all_orders():
    result = None
    
    return result

### Read Single Order

def get_order_by_id(id):
    result = None
    
    return result

### Update Single Order

def update_order(id,data):
    result = None
    row = result.fetchone()
    
    data["orderID"] = row["orderID"]
    
    return data

### Delete Single Order

def delete_order(id):
    
    result = execute(None)
    result.fetchone()
    
    return result.rowcount > 0