import mysql.connector
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mayur@6611",
    database="pharmacy"
)
cur = con.cursor()

def register():
    print("\n===== Registration =====")

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

def login():
    print("\n===== LOGIN =====")

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

con.close()
