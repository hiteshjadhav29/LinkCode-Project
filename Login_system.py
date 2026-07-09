import mysql.connector
from database import conn,cursor
# con = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="mayur@6611",
#     database="pharmacy"
# )
# cur = con.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role ENUM('Admin','User') NOT NULL
    );
""")
# cursor.execute("""
#     INSERT INTO login (username, password, role) VALUES
#     ('admin', 'admin123', 'Admin'),
#     ('user1', 'user123', 'User'),
#     ('mayuresh', 'mayur123', 'Admin'),
#     ('hitesh', 'hitesh123', 'Admin');
# """)
conn.commit()

def register():
    print("\n===== Registration =====")

    username = input("Enter Username : ")
    password = input("Enter Password : ")
    role = input("Enter Role (Admin/User) : ")

    sql = "INSERT INTO login(username,password,role) VALUES(%s,%s,%s)"
    val = (username, password, role)

    try:
        cursor.execute(sql, val)
        conn.commit()
        print("Registration Successful")
    except mysql.connector.IntegrityError:
        print("Username already exists!")

def login():
    print("\n===== LOGIN =====")

    
    username = input("Username: ")
    password = input("Password: ")
    role = input("Role (Admin/User): ")

    cursor.execute(
        "SELECT username, role FROM login WHERE username=%s AND password=%s AND role=%s",
        (username, password, role)
    )

    result = cursor.fetchone()

    if result:
        print("Login Successful")
        return result[1]      # "Admin" or "User"

    print("Invalid Username or Password")
    return None
    
def login_menu():
    while True:
        print("\n===== PHARMACY MANAGEMENT SYSTEM =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = int(input("Enter Your Choice : "))

        if choice == 1:
            register()

        elif choice == 2:
            login()

        elif choice == 3:
            print("Thank You!")
            break

        else:
            print("Invalid Choice")


