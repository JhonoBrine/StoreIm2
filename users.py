from database import fetchall, fetchone, execute
users = [
        {
            "id": 1,
            "name": "John",
            "email": "john@doe.com",
            "password": "123456"
        },
        {
            "id": 2,
            "name": "Jane",
            "email": "jane@doe.com",
            "password": "123456"
        },
        {
            "id": 3,
            "name": "Jake",
            "email": "jake@doe.com",
            "password": "123456"
        },
    ]
"""
CREATE TABLE `students` (
    `student_id` int NOT NULL AUTO_INCREMENT,
    `first_name` varchar(200) DEFAULT NULL,
    `last_name` varchar(200) DEFAULT NULL,
    `email` varchar(200) DEFAULT NULL,
    `birthdate` date DEFAULT NULL,
    `department_id` int DEFAULT NULL,
    PRIMARY KEY (`student_id`),
    KEY `department_id_idx` (`department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3

CREATE VIEW students_view As
    SELECT stud.student_id, stud.first_name, stud.last_name, stud.email, dep.department_name
    FROM students AS stud
    INNER JOIN departments AS dep ON stud.department_id = dep.department_id

CREATE PROCEDURE create_students(
    IN p_first_name varchar(200),
    IN p_last_name varchar(200),
    IN p_email varchar(200),
    IN p_birthdate date,
    IN p_department_id INT
)

BEGIN
    DECLARE p_students_id INT;
    INSERT INTO students (first_name, last_name, email, birthdate, department_id)
      VALUES (p_first_name, p_last_name, p_email, p_birthdate, p_department_id);
    SET p_students_id = LAST_INSERT_ID();
    SELECT p_students_id AS student_id;
END

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_students`(
  IN p_student_id INT,
  IN p_first_name varchar(200),
  IN p_last_name varchar(200),
  IN p_email varchar(200),
  IN p_birthdate date,
  IN p_department_id INT
)
BEGIN
  UPDATE students
    SET first_name = p_first_name,
		  last_name = p_last_name,
		  email = p_email,
		  birthdate = p_birthdate,
		  department_id = p_department_id
  WHERE student_id = p_student_id;
  SELECT p_student_id AS student_id;
END


"""
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
  # @TODO - replace this with a database call DELETE
  cur = execute("""DELETE FROM students WHERE student_id = %s""", (id,))
  cur.fetchone()
  
  return cur.rowcount > 0
