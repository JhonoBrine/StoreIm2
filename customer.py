from database import fetchall, fetchone, execute

### Create Customers

def create_customers(data):
    result = execute("""CALL create_customer(%s, %s, %s)""", (data["custFname"], data["custLname"], data["isMember"]))
    row = result.fetchone()
    data["custID"] = row["custID"]
    
    return data

### Read all Customers' List

def get_all_customers():
    result = fetchall("""SELECT * FROM customer_view""")
    return result

### Read Single Customer

def get_customer_by_id(id):
    result = fetchone("""SELECT * FROM customer_view WHERE custID = %s""", (id, ))
    return result

### Update Single Customer

def update_customer(id, data):
    result = execute("""CALL update_customer(%s, %s, %s, %s)""", (id, data["custFname"], data["custLname"], data["isMember"]))
    row = result.fetchone()
    data["custID"] = row["custID"]
    return data

### Delete a Single Customer

def delete_customer(id):
    result = execute("""DELETE FROM customer WHERE custID = %s""", (id, ))
    result.fetchone()
    
    return result.rowcount > 0