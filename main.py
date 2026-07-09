from Login_system import register, login
from Inventory_Management import inventory_menu
from employee_management import employee_menu
from Expiry_management import expiry_menu
from report import reports_menu
from sale_management import sale_menu


def admin_menu():
    while True:

        print("\n" + "=" * 50)
        print("      PHARMACY MANAGEMENT SYSTEM")
        print("=" * 50)

        print("1. Inventory Management")
        print("2. Sales & Billing")
        print("3. Employee Management")
        print("4. Expiry Management")
        print("5. Reports")
        print("6. Logout")

        choice = input("Enter Choice : ")

        if choice == "1":
            inventory_menu()

        elif choice == "2":
            sale_menu()

        elif choice == "3":
            employee_menu()

        elif choice == "4":
            expiry_menu()

        elif choice == "5":
            reports_menu()

        elif choice == "6":
            print("Logging Out...")
            break

        else:
            print("Invalid Choice")


def user_menu():
    while True:

        print("\n" + "=" * 50)
        print("          USER MENU")
        print("=" * 50)

        print("1. Sales & Billing")
        print("2. View Inventory")
        print("3. Logout")

        choice = input("Enter Choice : ")

        if choice == "1":
            sale_menu()

        elif choice == "2":
            inventory_menu()

        elif choice == "3":
            print("Logging Out...")
            break

        else:
            print("Invalid Choice")


def main():

    while True:

        print("\n" + "=" * 50)
        print("     PHARMACY MANAGEMENT SYSTEM")
        print("=" * 50)

        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter Choice : ")

        if choice == "1":
            register()

        elif choice == "2":

            role = login()

            if role == "Admin":
                admin_menu()

            elif role == "User":
                user_menu()

        elif choice == "3":

            print("Thank You For Using Pharmacy Management System")
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()