import mysql.connector
from database import conn,cursor
from Expiry_management import *
from Inventory_Management import *
from Login_system import *
from report import *
from sale_management import *
from tabulate import tabulate

cursor.execute("""
CREATE TABLE IF NOT EXISTS employee(
               emp_id INT PRIMARY KEY,
               emp_name VARCHAR(100),
               department VARCHAR(100),
               designation VARCHAR(100),
               salary DECIMAL(10,2)
)
""")

conn.commit()


def add_employee():
    emp_id = int(input("Enter Employee ID: "))
    emp_name = input("Enter Employee Name: ")
    department = input("Enter Department: ")
    designation = input("Enter Designation: ")
    salary = float(input("Enter Salary: "))

    query = "INSERT INTO employee (emp_id, emp_name, department, designation, salary) VALUES (%s, %s, %s, %s, %s)"
    values = (emp_id, emp_name, department, designation, salary)

    cursor.execute(query, values)
    conn.commit()

    print("Employee added successfully!")


def view_employee():
    cursor.execute("SELECT * FROM employee")
    records = cursor.fetchall()

    if records:
        headers = [
            "Employee ID",
            "Employee Name",
            "Department",
            "Designation",
            "Salary"
        ]

        print(tabulate(records, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No employee records found.")


def update_employee():
    emp_id = int(input("Enter Employee ID: "))

    cursor.execute(
        "SELECT * FROM employee WHERE emp_id=%s",
        (emp_id,)
    )

    if cursor.fetchone():

        name = input("Enter New Name: ")
        department = input("Enter Department: ")
        designation = input("Enter Designation: ")
        salary = float(input("Enter Salary: "))

        cursor.execute("""
        UPDATE employee
        SET emp_name=%s,
            department=%s,
            designation=%s,
            salary=%s
        WHERE emp_id=%s
        """, (name, department, designation, salary, emp_id))

        conn.commit()

        print("Employee Updated Successfully")

    else:
        print("Employee Not Found")

def delete_employee():
    emp_id = int(input("Enter Employee ID to delete: "))

    # query = "DELETE FROM employee WHERE emp_id=%s"
    # values = (emp_id,)

    cursor.execute(
    "SELECT * FROM employee WHERE emp_id=%s",
    (emp_id,)
)

    if cursor.fetchone():

        cursor.execute(
            "DELETE FROM employee WHERE emp_id=%s",(emp_id,)
        )

        conn.commit()

        print("Employee Deleted Successfully")

    else:
        print("Employee Not Found")


def search_employee():
    def search_by_id():
        emp_id = int(input("Enter Employee ID: "))

        cursor.execute(
            "SELECT * FROM employee WHERE emp_id=%s",
            (emp_id,)
        )

        record = cursor.fetchone()

        if record:
            headers = [
                "Employee ID",
                "Employee Name",
                "Department",
                "Designation",
                "Salary"
            ]

            print(tabulate([record], headers=headers, tablefmt="fancy_grid"))
        else:
            print("Employee Not Found")

    def search_by_name():
        name = input("Enter Employee Name: ")

        cursor.execute(
            "SELECT * FROM employee WHERE emp_name LIKE %s",
            ("%" + name + "%",)
        )

        records = cursor.fetchall()

        if records:
            headers = [
                "Employee ID",
                "Employee Name",
                "Department",
                "Designation",
                "Salary"
            ]

            print(tabulate(records, headers=headers, tablefmt="fancy_grid"))
        else:
            print("Employee Not Found")

    choice=0
    while choice!=3:
        print("1.Search by id\n2.Search by name\n3.exit")
        choice=int(input("enter choice"))
        match choice:
            case 1:
                search_by_id()
            case 2:
                search_by_name()
            case 3:
                break


def employee_menu():
    while True:
        print("\n===== Employee Management System =====")
        print("1. Add Employee")
        print("2. View Employee")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Search Employee")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_employee()

        elif choice == "2":
            view_employee()

        elif choice == "3":
            update_employee()

        elif choice == "4":
            delete_employee()

        elif choice == "5":
            search_employee()

        elif choice == "6":
            print("Thank You!")
            break

        else:
            print("Invalid Choice! Please try again.")
        
