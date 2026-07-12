import mysql.connector
from database import conn,cursor
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
from Expiry_management import *
from Inventory_Management import *
from Login_system import *
from employee_management import *
from sale_management import *


def create_tables():
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
        table_data.append([
            row[0],  # Medicine ID
            row[1],  # Medicine Name
            row[2],  # Category
            row[3],  # Quantity
            row[5],  # Selling Price
            row[6]   # Expiry Date
        ])

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

                break

            case _:

                print("Invalid Choice")