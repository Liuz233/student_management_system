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
# cursor.execute("DROP TABLE IF EXISTS enrollments CASCADE")
# cursor.execute("DROP TABLE IF EXISTS courses CASCADE")
# cursor.execute("DROP TABLE IF EXISTS students CASCADE")
# 获取查询结果
# results = cursor.fetchall()

# for row in results:
#     print(row)
# cursor.execute("SHOW DATABASES")
cursor.execute("""
    CREATE TABLE students (
        student_id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        enrollment_data DATE NOT NULL,
        major VARCHAR(50) NOT NULL,
        awards_and_punishments TEXT
    )
""")

# 创建课程表
cursor.execute("""
    CREATE TABLE courses (
        course_id VARCHAR(20) PRIMARY KEY,
        course_name VARCHAR(50) NOT NULL,
        instructor VARCHAR(50) NOT NULL,
        year_offered INT NOT NULL,
        credits INT NOT NULL
    )
""")

# 创建选课表
cursor.execute("""
    CREATE TABLE enrollments (
        student_id VARCHAR(20),
        course_id VARCHAR(20),
        grade FLOAT,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
    )
""")
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    print(table[0])
student_data = [
    ("S001", "John Doe", "2023-09-01", "Computer Science", "Dean's List, 2023"),
    ("S002", "Jane Smith", "2023-09-01", "Mathematics", "Dean's List, 2023"),
    ("S003", "Bob Johnson", "2023-09-01", "English", "Dean's List, 2023")
]
# 插入学生数据
cursor.executemany("INSERT INTO students (student_id, name, enrollment_data, major, awards_and_punishments) VALUES (%s, %s, %s, %s, %s)", student_data)

# # 插入课程数据
# cursor.execute("INSERT INTO courses (course_name, course_code, credits) VALUES (%s, %s, %s)", ("Introduction to Computer Science", "CS101", 3))
# cursor.execute("INSERT INTO courses (course_name, course_code, credits) VALUES (%s, %s, %s)", ("Calculus I", "MATH101", 4))
# cursor.execute("INSERT INTO courses (course_name, course_code, credits) VALUES (%s, %s, %s)", ("English Composition", "ENG101", 3))

# # 插入选课数据
# cursor.execute("INSERT INTO enrollments (student_id, course_id, semester) VALUES (%s, %s, %s)", ("S001", 1, "Fall 2023"))
# cursor.execute("INSERT INTO enrollments (student_id, course_id, semester) VALUES (%s, %s, %s)", ("S001", 2, "Fall 2023"))
# cursor.execute("INSERT INTO enrollments (student_id, course_id, semester) VALUES (%s, %s, %s)", ("S002", 1, "Spring 2023"))
# cursor.execute("INSERT INTO enrollments (student_id, course_id, semester) VALUES (%s, %s, %s)", ("S003", 3, "Fall 2023"))

db.commit()
db.close()