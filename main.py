from flask import Flask, request, jsonify, current_app
from users import get_all_users, get_user_by_id, create_user, update_user, delete_user
from flask_mysqldb import MySQL
from database import set_database


app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_PORT"] = "3306"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "mydb"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_AUTOCOMMIT"] = True


mysql = MySQL()
mysql.init_app(app)
set_database(mysql)

@app.route("/")
def home():
  return "<h1>Hello, CSIT327!</h1>"

@app.route("/users", methods=["GET", "POST"])
def users():
  if request.method == "POST":
    data = request.get_json()
    result = create_user(data)
  else:
    result = get_all_users()
  return jsonify(result)

@app.route("/users/<id>", methods=["GET", "PUT", "DELETE"])
def users_by_id(id):
  if request.method == "PUT":
    data = request.get_json()
    data["id"] = id
    result = update_user(id, data)
  elif request.method == "DELETE":
    result = delete_user(id)
  else:
    result = get_user_by_id(id)
  return jsonify(result)