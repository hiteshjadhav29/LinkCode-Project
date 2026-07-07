import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mayur@6611",   
    database="pharmacy"
)

if con.is_connected():
    print("Database Connected Successfully")

con.close()
