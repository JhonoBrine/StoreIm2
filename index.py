from flask import Flask, request, jsonify, current_app
from item import get_all_items, get_item_by_id, create_item, update_item, delete_item
from flask_mysqldb import MySQL
from database import set_database
from dotenv import load_dotenv
from os import getenv

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