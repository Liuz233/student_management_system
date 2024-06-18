import mysql.connector

# 连接 MySQL 数据库
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="wo20030426",
    port = 3306
)
cursor = db.cursor()
# cursor.execute("CREATE DATABASE student_management_system")
cursor.execute("USE student_management_system")
student_data = [
    ("S001", "John Doe", "2023-09-01", "Computer Science", "Dean's List, 2023"),
    ("S002", "Jane Smith", "2023-09-01", "Mathematics", "Dean's List, 2023"),
    ("S003", "Bob Johnson", "2023-09-01", "English", "Dean's List, 2023")
]
courses_data = [
    ("C001", "Introduction to Computer Science", "Dr. Smith", 2023, 3),
    ("C002", "Calculus I", "Dr. Johnson", 2023, 4),
    ("C003", "English Composition", "Dr. Brown", 2023, 3)
]
enrollments_data = [
    ("S001", "C001", 3.7),
    ("S001", "C002", 4.0),
    ("S002", "C001", 3.7),
    ("S002", "C003", 3.7),
    ("S003", "C002", 3.7),
    ("S003", "C003", 3.0)
]
# 插入学生数据
# cursor.executemany("INSERT INTO students (student_id, name, enrollment_data, major, awards_and_punishments) VALUES (%s, %s, %s, %s, %s)", student_data)
# 插入课程数据
#cursor.executemany("INSERT INTO courses (course_id, course_name, instructor, year_offered, credits) VALUES (%s, %s, %s, %s, %s)", courses_data)
# 插入选课数据
cursor.executemany("INSERT INTO enrollments (student_id, course_id, grade) VALUES (%s, %s, %s)", enrollments_data)
db.commit()
db.close()