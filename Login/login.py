import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mayur@6611",    
    database="pharmacy"
)

cur = con.cursor()

print("===== LOGIN =====")

username = input("Enter Username : ")
password = input("Enter Password : ")
role = input("Enter Role (Admin/User) : ")

sql = "SELECT * FROM login WHERE username=%s AND password=%s AND role=%s"
val = (username, password, role)

cur.execute(sql, val)

result = cur.fetchone()

if result:
    print("\nLogin Successful")
    print("Welcome", result[1])
else:
    print("\nInvalid Username or Password")

con.close()
