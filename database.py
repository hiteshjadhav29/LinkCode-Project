import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    username="root",
    password="Hitesh@29",   
    database="linkcode_project"
)
cursor=conn.cursor()

if conn.is_connected():
    print("Database Connected Successfully")


