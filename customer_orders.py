from database import fetchall, fetchone, execute

### VIEW RA NI

def view_customer_orders_by_id(id):
    result = fetchone("""SELECT * FROM customer_orders_view WHERE custID = %s""", (id,))
    return result

### VIEW ALL RA NI

def view_customer_orders():
    result = fetchall("""SELECT * FROM customer_orders_view""")
    return result
