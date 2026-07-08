import sqlite3
# Database Connection

conn = sqlite3.connect("pharmacy.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines(
    medicine_id INTEGER PRIMARY KEY,
    medicine_name TEXT NOT NULL,
    category TEXT,
    quantity INTEGER,
    price REAL,
    expiry_date TEXT
)
""")

conn.commit()
# Add Medicine
def add_medicine():
    try:
        medicine_id = int(input("Enter Medicine ID: "))
        medicine_name = input("Enter Medicine Name: ")
        category = input("Enter Category (Tablet/Syrup/Injection): ")
        quantity = int(input("Enter Quantity: "))
        price = float(input("Enter Price: "))
        expiry_date = input("Enter Expiry Date (DD/MM/YYYY): ")

        cursor.execute("""
        INSERT INTO medicines
        VALUES(?,?,?,?,?,?)
        """, (medicine_id, medicine_name, category,
              quantity, price, expiry_date))

        conn.commit()

        print("\nMedicine Added Successfully!")

    except sqlite3.IntegrityError:
        print("\nMedicine ID already exists!")



# View Medicines
def view_medicines():

    cursor.execute("SELECT * FROM medicines")

    medicines = cursor.fetchall()

    if len(medicines) == 0:
        print("\nNo Medicines Available")
    else:
        print("\n----------- Medicine List -----------")

        for medicine in medicines:
            print("-----------------------------------")
            print("Medicine ID :", medicine[0])
            print("Name        :", medicine[1])
            print("Category    :", medicine[2])
            print("Quantity    :", medicine[3])
            print("Price       :", medicine[4])
            print("Expiry Date :", medicine[5])


# Search by ID

def search_by_id():

    medicine_id = int(input("Enter Medicine ID: "))

    cursor.execute(
        "SELECT * FROM medicines WHERE medicine_id=?",
        (medicine_id,)
    )

    medicine = cursor.fetchone()

    if medicine:
        print("\nMedicine Found")
        print(medicine)
    else:
        print("\nMedicine Not Found")


# Search by Name
def search_by_name():

    name = input("Enter Medicine Name: ")

    cursor.execute(
        "SELECT * FROM medicines WHERE medicine_name LIKE ?",
        ('%' + name + '%',)
    )

    medicines = cursor.fetchall()

    if medicines:

        print("\nMedicine Found")

        for medicine in medicines:
            print(medicine)

    else:
        print("\nMedicine Not Found")

# Update Medicine
def update_medicine():

    medicine_id = int(input("Enter Medicine ID: "))

    cursor.execute(
        "SELECT * FROM medicines WHERE medicine_id=?",
        (medicine_id,)
    )

    medicine = cursor.fetchone()

    if medicine:

        print("\nEnter New Details")

        new_name = input("New Medicine Name: ")
        new_price = float(input("New Price: "))
        new_expiry = input("New Expiry Date: ")

        cursor.execute("""
        UPDATE medicines
        SET medicine_name=?,
            price=?,
            expiry_date=?
        WHERE medicine_id=?
        """, (new_name, new_price, new_expiry, medicine_id))

        conn.commit()

        print("\nMedicine Updated Successfully!")

    else:
        print("\nMedicine Not Found")



# Delete Medicine

def delete_medicine():

    medicine_id = int(input("Enter Medicine ID: "))

    cursor.execute(
        "SELECT * FROM medicines WHERE medicine_id=?",
        (medicine_id,)
    )

    medicine = cursor.fetchone()

    if medicine:

        cursor.execute(
            "DELETE FROM medicines WHERE medicine_id=?",
            (medicine_id,)
        )

        conn.commit()

        print("\nMedicine Deleted Successfully!")

    else:
        print("\nMedicine Not Found")


# Check Stock
def check_stock():

    cursor.execute("""
    SELECT medicine_name, quantity
    FROM medicines
    """)

    medicines = cursor.fetchall()

    if medicines:

        print("\n------ Available Stock ------")

        for medicine in medicines:
            print(f"{medicine[0]} : {medicine[1]} Units")

    else:
        print("\nNo Medicines Available")

# Main Menu
while True:

    print("\n===================================")
    print(" PHARMACY INVENTORY MANAGEMENT")
    print("===================================")
    print("1. Add Medicine")
    print("2. View All Medicines")
    print("3. Search Medicine by ID")
    print("4. Search Medicine by Name")
    print("5. Update Medicine")
    print("6. Delete Medicine")
    print("7. Check Stock Quantity")
    print("8. Exit")

    choice = input("\nEnter Your Choice: ")

    if choice == '1':
        add_medicine()

    elif choice == '2':
        view_medicines()

    elif choice == '3':
        search_by_id()

    elif choice == '4':
        search_by_name()

    elif choice == '5':
        update_medicine()

    elif choice == '6':
        delete_medicine()

    elif choice == '7':
        check_stock()

    elif choice == '8':
        print("\nThank You for Using Pharmacy Management System!")
        break

    else:
        print("\nInvalid Choice! Please Try Again.")

conn.close()
