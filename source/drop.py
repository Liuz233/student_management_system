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
cursor.execute("DROP TABLE IF EXISTS enrollments CASCADE")
cursor.execute("DROP TABLE IF EXISTS courses CASCADE")
cursor.execute("DROP TABLE IF EXISTS students CASCADE")