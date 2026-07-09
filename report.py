import mysql.connector
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hitesh@29",
    database="linkcode_project"
)

cursor = conn.cursor()
def create_tables():

    # Medicine Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicine(
        medicine_id INT AUTO_INCREMENT PRIMARY KEY,
        medicine_name VARCHAR(100),
        category VARCHAR(50),
        quantity INT,
        purchase_price DECIMAL(10,2),
        price DECIMAL(10,2),
        expiry_date DATE
    )
    """)

    # Sales Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales(
        sale_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_name VARCHAR(100),
        customer_contact VARCHAR(15),
        medicine_id INT,
        medicine_name VARCHAR(100),
        quantity_sold INT,
        price_per_unit DECIMAL(10,2),
        total_amount DECIMAL(10,2),
        sale_date DATE,
        payment_method VARCHAR(20)
    )
    """)

    # Report History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS report_history(
        report_id INT AUTO_INCREMENT PRIMARY KEY,
        report_type VARCHAR(50),
        generated_by VARCHAR(50),
        generated_on DATETIME DEFAULT CURRENT_TIMESTAMP,
        file_name VARCHAR(255)
    )
    """)

    conn.commit()

    print("All Required Tables Created Successfully")
create_tables()
cursor.execute("""
INSERT INTO medicine
(medicine_name, category, quantity, purchase_price, price, expiry_date)
VALUES
('Paracetamol 500mg','Tablet',120,8.50,12.00,'2027-12-31'),
('Amoxicillin 250mg','Capsule',75,18.00,25.00,'2027-10-15'),
('Cetirizine 10mg','Tablet',45,4.00,7.50,'2027-09-20'),
('Cough Syrup','Syrup',30,55.00,80.00,'2027-08-25'),
('Insulin Injection','Injection',18,420.00,550.00,'2027-07-30'),
('Vitamin C','Tablet',150,3.00,5.00,'2028-01-10'),
('ORS Powder','Powder',60,12.00,18.00,'2027-11-18'),
('Pain Relief Gel','Gel',25,45.00,65.00,'2027-12-15'),
('Eye Drops','Drops',40,35.00,55.00,'2027-10-05'),
('Multivitamin','Capsule',95,15.00,24.00,'2028-02-14')
""")
cursor.execute("""
INSERT INTO sales
(customer_name, customer_contact, medicine_id, medicine_name,
quantity_sold, price_per_unit, total_amount, sale_date, payment_method)
VALUES
('Rahul Sharma','9876543210',1,'Paracetamol 500mg',5,12.00,60.00,'2026-07-01','Cash'),

('Priya Patil','9988776655',2,'Amoxicillin 250mg',3,25.00,75.00,'2026-07-02','UPI'),

('Amit Joshi','9123456789',4,'Cough Syrup',2,80.00,160.00,'2026-07-03','Card'),

('Sneha Kulkarni','9001122334',5,'Insulin Injection',1,550.00,550.00,'2026-07-04','Cash'),

('Rohit Deshmukh','9090909090',6,'Vitamin C',10,5.00,50.00,'2026-07-05','UPI'),

('Neha Pawar','9876501234',3,'Cetirizine 10mg',6,7.50,45.00,'2026-07-05','Cash'),

('Saurabh Singh','9988007766',7,'ORS Powder',4,18.00,72.00,'2026-07-06','Card'),

('Pooja More','9871234567',8,'Pain Relief Gel',2,65.00,130.00,'2026-07-06','UPI'),

('Karan Shah','9900112233',9,'Eye Drops',1,55.00,55.00,'2026-07-07','Cash'),

('Anjali Verma','9765432109',10,'Multivitamin',5,24.00,120.00,'2026-07-07','Card')
""")
cursor.execute("""
INSERT INTO report_history
(report_type, generated_by, file_name)
VALUES
('Inventory Report','Admin','Inventory_Report.pdf'),
('Sales Report','Admin','Sales_Report.pdf'),
('Low Stock Report','Admin','Low_Stock_Report.pdf'),
('Profit Report','Admin','Profit_Report.pdf')
""")
conn.commit()

styles = getSampleStyleSheet()
def save_report(report_type, filename):

    sql = """
    INSERT INTO report_history(report_type,generated_by,file_name)
    VALUES(%s,%s,%s)
    """

    cursor.execute(sql,(report_type,"Admin",filename))
    conn.commit()

def inventory_report():

    cursor.execute("SELECT * FROM medicine")

    data = cursor.fetchall()

    filename = "Inventory_Report.pdf"

    doc = SimpleDocTemplate(filename)

    elements=[]

    elements.append(Paragraph("<b>Inventory Report</b>",styles['Title']))
    elements.append(Spacer(1,0.2*inch))

    table_data=[]

    table_data.append([
        "ID",
        "Medicine",
        "Category",
        "Quantity",
        "Price",
        "Expiry"
    ])

    for row in data:
        table_data.append(row)

    table=Table(table_data)

    table.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,0),colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ('ALIGN',(0,0),(-1,-1),'CENTER')

    ]))

    elements.append(table)

    doc.build(elements)

    save_report("Inventory",filename)

    print("Inventory Report Generated.")

def sales_report():

    cursor.execute("SELECT * FROM sales")

    data=cursor.fetchall()

    filename="Sales_Report.pdf"

    doc=SimpleDocTemplate(filename)

    elements=[]

    elements.append(Paragraph("<b>Sales Report</b>",styles['Title']))
    elements.append(Spacer(1,0.2*inch))

    table_data=[[
        "Sale ID",
        "Customer",
        "Medicine",
        "Qty",
        "Price",
        "Total",
        "Date",
        "Payment"
    ]]

    for row in data:

        table_data.append([
            row[0],
            row[1],
            row[4],
            row[5],
            row[6],
            row[7],
            str(row[8]),
            row[9]
        ])

    table=Table(table_data)

    table.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('BACKGROUND',(0,0),(-1,0),colors.darkblue),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ]))

    elements.append(table)

    doc.build(elements)

    save_report("Sales",filename)

    print("Sales Report Generated.")

def low_stock_report():

    cursor.execute(
        "SELECT medicine_id,medicine_name,quantity FROM medicine WHERE quantity<20"
    )

    data=cursor.fetchall()

    filename="Low_Stock_Report.pdf"

    doc=SimpleDocTemplate(filename)

    elements=[]

    elements.append(Paragraph("<b>Low Stock Report</b>",styles['Title']))
    elements.append(Spacer(1,0.2*inch))

    table_data=[

        ["Medicine ID","Medicine Name","Quantity"]

    ]

    for row in data:
        table_data.append(row)

    table=Table(table_data)

    table.setStyle(TableStyle([

        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('BACKGROUND',(0,0),(-1,0),colors.red),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER')

    ]))

    elements.append(table)

    doc.build(elements)

    save_report("Low Stock",filename)

    print("Low Stock Report Generated.")

def profit_report():

    cursor.execute("""

    SELECT
    m.medicine_name,
    SUM(s.quantity_sold),
    m.purchase_price,
    m.price

    FROM sales s

    JOIN medicine m

    ON s.medicine_id=m.medicine_id

    GROUP BY s.medicine_id

    """)

    data=cursor.fetchall()

    filename="Profit_Report.pdf"

    doc=SimpleDocTemplate(filename)

    elements=[]

    elements.append(Paragraph("<b>Profit Report</b>",styles['Title']))
    elements.append(Spacer(1,0.2*inch))

    table_data=[

        [
            "Medicine",
            "Sold",
            "Purchase Price",
            "Selling Price",
            "Profit"
        ]

    ]

    total_profit=0

    for row in data:

        profit=(row[3]-row[2])*row[1]

        total_profit+=profit

        table_data.append([

            row[0],
            row[1],
            row[2],
            row[3],
            round(profit,2)

        ])

    table_data.append(["","","","Total Profit",round(total_profit,2)])

    table=Table(table_data)

    table.setStyle(TableStyle([

        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('BACKGROUND',(0,0),(-1,0),colors.green),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER')

    ]))

    elements.append(table)

    doc.build(elements)

    save_report("Profit",filename)

    print("Profit Report Generated.")

def reports_menu():
    ch=0
    while ch!=6:

        print("\n===== REPORT MENU =====")

        print("1.Inventory Report")

        print("2.Sales Report")

        print("3.Low Stock Report")

        print("4.Profit Report")

        print("5.View Report History")

        print("6.Exit")

        ch=int(input("Enter Choice : "))

        match ch:
            case 1:

                inventory_report()

            case 2:     

                sales_report()

            case 3:

                low_stock_report()

            case 4:

                profit_report()

            case 5:

                cursor.execute("SELECT * FROM report_history")

                for row in cursor.fetchall():

                    print(row)

            case 6:

                exit(0)

            case _:

                print("Invalid Choice")