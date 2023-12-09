from database import fetchall, fetchone, execute

### VIEW RA NI

def view_customer_orders(id):
    result = fetchone("""SELECT * FROM customer_orders_view WHERE custID = %s""", (id,))
    return result

