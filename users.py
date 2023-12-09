from database import fetchall, fetchone, execute

def create_user(data):
    cur = execute("""CALL create_students(%s, %s, %s, %s, %s)""", (data["first_name"], data["last_name"], data["email"], data["birthdate"], data["department_id"]))
    row = cur.fetchone()
    data["student_id"] = row["student_id"]
    
    return data

def get_user_by_id(id):
    rv = fetchone("""SELECT * FROM studentdepartment_view WHERE student_id = %s""", (id,))
    return rv

def get_all_users():
    rv = fetchall("""SELECT * FROM studentdepartment_view""")

    return rv

def update_user(id, data):
  cur = execute("""CALL update_students(%s, %s, %s, %s, %s, %s)""", (id, data["first_name"], data["last_name"], data["email"], data["birthdate"], data["department_id"]))
  
  row = cur.fetchone()
  data["student_id"] = row["student_id"]
  return data

def delete_user(id):

  cur = execute("""DELETE FROM students WHERE student_id = %s""", (id,))
  cur.fetchone()
  
  return cur.rowcount > 0
