mysql = None


def set_database(mysql_instance):
    global mysql
    mysql = mysql_instance
    
def get_connection():
    return mysql.connection

def execute(query, params=()):
    cur = get_cursor()
    cur.execute(query, params)
    return cur

def get_cursor():
    return mysql.connection.cursor()

def fetchall(query, params=()):
    cur = execute(query, params)
    return cur.fetchall()
    

def fetchone(query, params=()):
    cur = execute(query, params)
    return cur.fetchall()