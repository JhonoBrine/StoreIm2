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