import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="192008",
    database="pharmacy_db"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines(
medicine_id INT PRIMARY KEY,
medicine_name VARCHAR(100) NOT NULL,
category VARCHAR(50),
quantity INT,
price DECIMAL(10,2),
expiry_date DATE
)
""")
conn.commit()

def add_medicine():
    try:
        mid=int(input("Medicine ID: "))
        name=input("Medicine Name: ")
        cat=input("Category: ")
        qty=int(input("Quantity: "))
        price=float(input("Price: "))
        exp=input("Expiry Date (YYYY-MM-DD): ")
        cursor.execute("INSERT INTO medicines VALUES(%s,%s,%s,%s,%s,%s)",
                       (mid,name,cat,qty,price,exp))
        conn.commit()
        print("Medicine Added Successfully!")
    except mysql.connector.Error as e:
        print("Error:",e)

def view_medicines():
    cursor.execute("SELECT * FROM medicines")
    rows=cursor.fetchall()
    if not rows:
        print("No Medicines Found")
    for r in rows:
        print(r)

def search_by_id():
    mid=int(input("Medicine ID: "))
    cursor.execute("SELECT * FROM medicines WHERE medicine_id=%s",(mid,))
    r=cursor.fetchone()
    print(r if r else "Medicine Not Found")

def search_by_name():
    name=input("Medicine Name: ")
    cursor.execute("SELECT * FROM medicines WHERE medicine_name LIKE %s",('%'+name+'%',))
    rows=cursor.fetchall()
    if rows:
        for r in rows: print(r)
    else:
        print("Medicine Not Found")

def update_medicine():
    mid=int(input("Medicine ID: "))
    cursor.execute("SELECT * FROM medicines WHERE medicine_id=%s",(mid,))
    if cursor.fetchone():
        name=input("New Name: ")
        price=float(input("New Price: "))
        exp=input("New Expiry Date (YYYY-MM-DD): ")
        cursor.execute("UPDATE medicines SET medicine_name=%s,price=%s,expiry_date=%s WHERE medicine_id=%s",
                       (name,price,exp,mid))
        conn.commit()
        print("Updated Successfully!")
    else:
        print("Medicine Not Found")

def delete_medicine():
    mid=int(input("Medicine ID: "))
    cursor.execute("DELETE FROM medicines WHERE medicine_id=%s",(mid,))
    conn.commit()
    print("Deleted Successfully!")

def check_stock():
    cursor.execute("SELECT medicine_name,quantity FROM medicines")
    rows=cursor.fetchall()
    if not rows:
        print("No Medicines Available")
    for n,q in rows:
        print(f"{n}: {q} Units")

while True:
    print("\nPHARMACY INVENTORY MANAGEMENT")
    print("1.Add Medicine")
    print("2.View Medicines")
    print("3.Search by ID")
    print("4.Search by Name")
    print("5.Update Medicine")
    print("6.Delete Medicine")
    print("7.Check Stock")
    print("8.Exit")
    ch=input("Enter Choice: ")

    if ch=="1": add_medicine()
    elif ch=="2": view_medicines()
    elif ch=="3": search_by_id()
    elif ch=="4": search_by_name()
    elif ch=="5": update_medicine()
    elif ch=="6": delete_medicine()
    elif ch=="7": check_stock()
    elif ch=="8":
        break
    else:
        print("Invalid Choice")

conn.close()
