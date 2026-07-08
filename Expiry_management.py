#database connection
import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="anushka@2212",
    database="pharmacy"
)


# View Expired Medicines

from db import *
def view_expired():

    query = """
    SELECT * FROM medicines
    WHERE expiry_date < CURDATE();
    """

    cursor.execute(query)

    records = cursor.fetchall()

    if len(records) == 0:
        print("\nNo expired medicines found.")
        return

    print("\n===== EXPIRED MEDICINES =====")

    for row in records:
        print(row)

# View Medicines Expiring
# Within Next 30 Days

def expiry_30_days():

    query = """
    SELECT * FROM medicines
    WHERE expiry_date BETWEEN CURDATE()
    AND DATE_ADD(CURDATE(), INTERVAL 30 DAY);
    """

    cursor.execute(query)

    records = cursor.fetchall()

    if len(records) == 0:
        print("\nNo medicines expiring within 30 days.")
        return

    print("\n===== EXPIRING WITHIN 30 DAYS =====")

    for row in records:
        print(row)


# Remove Expired Stock
def remove_expired():

    query = """
    SELECT * FROM medicines
    WHERE expiry_date < CURDATE();
    """

    cursor.execute(query)

    records = cursor.fetchall()

    if len(records) == 0:
        print("\nNo expired medicines to remove.")
        return

    print("\nExpired Medicines:")

    for row in records:
        print(row)

    confirm = input("\nRemove all expired medicines? (yes/no): ")

    if confirm.lower() == "yes":

        delete_query = """
        DELETE FROM medicines
        WHERE expiry_date < CURDATE();
        """

        cursor.execute(delete_query)

        con.commit()

        print("\nExpired medicines removed successfully.")

    else:
        print("\nOperation cancelled.")

# Main Menu
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
