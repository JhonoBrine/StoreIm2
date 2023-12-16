from flask import Flask, request, jsonify, current_app, render_template
from flask_mysqldb import MySQL
from database import set_database
from dotenv import load_dotenv
from os import getenv
from flask_cors import CORS

from item import get_all_items, get_item_by_id, create_item, update_item, delete_item
from customer import get_all_customers, get_customer_by_id, create_customers, update_customer, delete_customer
from order import get_all_orders, get_order_by_id, create_order, update_order, delete_order
from customer_orders import view_customer_orders, view_customer_orders_by_id

app = Flask(__name__)
CORS(app)

load_dotenv()
app.config["MYSQL_HOST"] = getenv("MYSQL_HOST")
# app.config["MYSQL_PORT"] = getenv("MYSQL_PORT")
app.config["MYSQL_USER"] = getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = getenv("MYSQL_DB")

app.config["MYSQL_CURSORCLASS"] = getenv("MYSQL_CURSORCLASS")
app.config["MYSQL_AUTOCOMMIT"] = True if getenv("MYSQL_AUTOCOMMIT") == "True" else False


mysql = MySQL()
mysql.init_app(app)
set_database(mysql)

@app.route("/")
def home():
  return render_template("index.html")


### ITEMS

@app.route("/items", methods=["GET", "POST"])
def items():
  if request.method == "POST":
    data = request.get_json()
    result = create_item(data)
  else:
    result = get_all_items()
  return jsonify(result)

@app.route("/items/<id>", methods=["GET", "PUT", "DELETE"])
def items_by_id(id):
  if request.method == "PUT":
    data = request.get_json()
    data["id"] = id
    result = update_item(id, data)
  elif request.method == "DELETE":
    result = delete_item(id)
  else:
    result = get_item_by_id(id)
  return jsonify(result)

### CUSTOMERS

@app.route("/customers", methods=["GET", "POST"])
def customers():
  if request.method == "POST":
    data = request.get_json()
    result = create_customers(data)
  else:
    result = get_all_customers()
  return jsonify(result)

@app.route("/customers/<id>", methods=["GET", "PUT", "DELETE"])
def customers_by_id(id):
  if request.method == "PUT":
    data = request.get_json()
    data["id"] = id
    result = update_customer(id, data)
  elif request.method == "DELETE":
    result = get_customer_by_id(id)
    if result is not None:
      result = delete_customer(id)
    else:
      result = {"error" : "Customer not found"}
  else:
    result = get_customer_by_id(id)
  return jsonify(result)


### ORDERS

@app.route("/orders", methods=["GET", "POST"])
def orders():
  if request.method == "POST":
    data = request.get_json()
    checkCustId =  get_customer_by_id(data["custID"])
    checkItemId = get_item_by_id(data["itemID"])
    
    if checkCustId is not None and checkItemId is not None:
      result = create_order(data)
    else:
      result = {"error" : "Customer or Item not found!"}
  else:
    result = get_all_orders()
  return jsonify(result)

@app.route("/orders/<id>", methods=["GET", "PUT", "DELETE"])
def orders_by_id(id):
  if request.method == "PUT":
    data = request.get_json()
    data["id"] = id
    result = update_order(id, data)
  elif request.method == "DELETE":
    result = delete_order(id)
  else:
    result = get_order_by_id(id)
  return jsonify(result)

### Customer Order

@app.route("/customer-order", methods=["GET"])
def customer_orders():
  result = view_customer_orders()
  return jsonify(result)

@app.route("/customer-order/<id>", methods=["GET"])
def customer_orders_by_id(id):
  result = view_customer_orders_by_id(id)
  return jsonify(result)


