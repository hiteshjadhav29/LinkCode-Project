import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@shru123",
    database="pharmacy"
)

cursor = conn.cursor()

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
        print("\nEmployee Records:")
        for row in records:
            print(row)
    else:
        print("No employee records found.")


def update_employee():
    emp_id = int(input("Enter Employee ID to update: "))
    new_salary = float(input("Enter New Salary: "))

    query = "UPDATE employee SET salary=%s WHERE emp_id=%s"
    values = (new_salary, emp_id)

    cursor.execute(query, values)
    conn.commit()

    print("Employee updated successfully!")


def delete_employee():
    emp_id = int(input("Enter Employee ID to delete: "))

    query = "DELETE FROM employee WHERE emp_id=%s"
    values = (emp_id,)

    cursor.execute(query, values)
    conn.commit()

    print("Employee deleted successfully!")

while True:
    print("\n===== Employee Management System =====")
    print("1. Add Employee")
    print("2. View Employee")
    print("3. Update Employee")
    print("4. Delete Employee")
    print("5. Exit")

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
        print("Thank You!")
        break

    else:
        print("Invalid Choice! Please try again.")
        
conn.close()    