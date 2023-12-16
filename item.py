from database import fetchall, fetchone, execute

### Create Item

def create_item(data):
    result = execute("""CALL create_item(%s, %s, %s)""", (data["itemName"], data["itemQuantity"], data["itemPrice"]))
    row = result.fetchone()
    data["itemID"] = row["itemID"]

    return data
### Read all Item List

def get_all_items():
    result = fetchall("""SELECT * FROM items_view""")
    
    return result

### Read Single Item

def get_item_by_id(id):
    result = fetchone("""SELECT * FROM items_view WHERE itemID = %s""", (id, ))
    
    return result

### Update Single Item

def update_item(id, data):
    result = execute("""CALL update_item(%s, %s, %s, %s)""", (id, data["itemName"], data["itemQuantity"], data["itemPrice"]))
    
    row = result.fetchone()
    data["itemID"] = row["itemID"]
    
    return data

### Delete Single Item

def delete_item(id):
    cur = execute("""CALL delete_item(%s)""", (id, ))
    row = cur.fetchone()
    if row is None:
        return True
    return False