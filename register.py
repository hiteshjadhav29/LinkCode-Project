import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mayur@6611",      
    database="pharmacy"
)

cur = con.cursor()

print("===== Registration =====")

username = input("Enter Username : ")
password = input("Enter Password : ")
role = input("Enter Role (Admin/User) : ")

sql = "INSERT INTO login(username,password,role) VALUES(%s,%s,%s)"
val = (username, password, role)

try:
    cur.execute(sql, val)
    con.commit()
    print("Registration Successful")
except mysql.connector.IntegrityError:
    print("Username already exists!")

con.close()
