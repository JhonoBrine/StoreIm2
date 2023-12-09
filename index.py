from flask import Flask, request, jsonify, current_app
from flask_mysqldb import MySQL
from database import set_database
from dotenv import load_dotenv
from os import getenv

from item import get_all_items, get_item_by_id, create_item, update_item, delete_item
from customer import get_all_customers, get_customer_by_id, create_customers, update_customer, delete_customer
from order import get_all_orders, get_order_by_id, create_order, update_order, delete_order
from customer_orders import view_customer_orders

app = Flask(__name__)

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
  return "<h1>Welcome to the Store Home Page</h1> </br> <h3>Created by Rey Mar and Friends</h3>"

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
    result = delete_customer(id)
  else:
    result = get_customer_by_id(id)
  return jsonify(result)


### ORDERS

@app.route("/orders", methods=["GET", "POST"])
def orders():
  if request.method == "POST":
    data = request.get_json()
    result = create_order(data)
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

@app.route("/customer-order/<id>", methods=["GET"])
def customer_orders(id):
  result = view_customer_orders(id)
  return jsonify(result)