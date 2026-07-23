#database connection
import mysql.connector
from database import conn,cursor
from employee_management import *
from Inventory_Management import *
from Login_system import *
from report import *
from sale_management import *
from tabulate import tabulate

def view_expired():

    query = """
    SELECT * FROM medicine
    WHERE expiry_date < CURDATE();
    """

    cursor.execute(query)
    records = cursor.fetchall()

    if not records:
        print("\nNo expired medicines found.")
        return

    headers = [
        "Medicine ID",
        "Medicine Name",
        "Category",
        "Quantity",
        "Price",
        "Expiry Date"
    ]

    formatted = []

    for row in records:
        formatted.append([
            row[0],
            row[1],
            row[2],
            row[3],
            f"₹{float(row[4]):,.2f}",
            row[5]
        ])

    print("\n===== EXPIRED MEDICINES =====\n")
    print(tabulate(formatted, headers=headers, tablefmt="fancy_grid"))

# View Medicines Expiring
# Within Next 30 Days

def expiry_30_days():

    query = """
    SELECT * FROM medicine
    WHERE expiry_date BETWEEN CURDATE()
    AND DATE_ADD(CURDATE(), INTERVAL 30 DAY);
    """

    cursor.execute(query)
    records = cursor.fetchall()

    if not records:
        print("\nNo medicines expiring within 30 days.")
        return

    headers = [
        "Medicine ID",
        "Medicine Name",
        "Category",
        "Quantity",
        "Price",
        "Expiry Date"
    ]

    formatted = []

    for row in records:
        formatted.append([
            row[0],
            row[1],
            row[2],
            row[3],
            f"₹{float(row[4]):,.2f}",
            row[5]
        ])

    print("\n===== MEDICINES EXPIRING WITHIN 30 DAYS =====\n")
    print(tabulate(formatted, headers=headers, tablefmt="fancy_grid"))


# Remove Expired Stock
def remove_expired():

    cursor.execute("""
        SELECT * FROM medicine
        WHERE expiry_date < CURDATE()
    """)

    records = cursor.fetchall()

    if not records:
        print("\nNo expired medicines to remove.")
        return

    headers = [
        "Medicine ID",
        "Medicine Name",
        "Category",
        "Quantity",
        "Price",
        "Expiry Date"
    ]

    formatted = []

    for row in records:
        formatted.append([
            row[0],
            row[1],
            row[2],
            row[3],
            f"₹{float(row[4]):,.2f}",
            row[5]
        ])

    print("\n===== EXPIRED MEDICINES =====\n")
    print(tabulate(formatted, headers=headers, tablefmt="fancy_grid"))

    confirm = input("\nRemove all expired medicines? (yes/no): ")

    if confirm.lower() == "yes":

        cursor.execute("""
            DELETE FROM medicine
            WHERE expiry_date < CURDATE()
        """)

        conn.commit()

        print("\nExpired medicines removed successfully.")

    else:
        print("\nOperation cancelled.")

# Main Menu
def expiry_menu():
    while True:

        print("\n")
        print("=" * 40)
        print("EXPIRY MANAGEMENT")
        print("=" * 40)

        print("1. View Expired Medicines")
        print("2. View Medicines Expiring in Next 30 Days")
        print("3. Remove Expired Stock")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_expired()

        elif choice == "2":
            expiry_30_days()

        elif choice == "3":
            remove_expired()

        elif choice == "4":
            print("\nThank you!")
            break

        else:
            print("\nInvalid Choice.")
