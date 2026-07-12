from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import mysql.connector
from database import conn,cursor
from Expiry_management import *
from Inventory_Management import *
from Login_system import *
from report import *
from employee_management import *
import smtplib
import os
from email.message import EmailMessage


cursor.execute("""
CREATE TABLE IF NOT EXISTS medicine(
    medicine_id INT PRIMARY KEY AUTO_INCREMENT,
    medicine_name VARCHAR(50),
    category VARCHAR(50),
    quantity INT,
    price FLOAT,
    expiry_date DATE
)
""")

conn.commit()

print("MySQL Database Connected Successfully")
print("Table Ready")


cart = []
bill_data = None


def add_medicine():

    name = input("Enter Medicine Name : ").strip()
    category = input("Enter Category : ").strip()

    try:
        quantity = int(input("Enter Quantity : "))
        price = float(input("Enter Price : "))
    except ValueError:
        print("Invalid quantity or price. Please enter numbers only.")
        return

    if not name or not category:
        print("Medicine name and category cannot be empty.")
        return

    expiry = None
    while expiry is None:
        raw_date = input("Enter Expiry Date (YYYY-MM-DD) : ").strip()
        try:
            datetime.strptime(raw_date, "%Y-%m-%d")
            expiry = raw_date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD, e.g. 2027-07-17.")

    cursor.execute("""
    INSERT INTO medicine
    (medicine_name,category,quantity,price,expiry_date)
    VALUES(%s,%s,%s,%s,%s)
    """, (name, category, quantity, price, expiry))

    conn.commit()

    print("Medicine Added Successfully")


def view_medicines():

    cursor.execute("SELECT * FROM medicine")

    data = cursor.fetchall()

    if len(data) == 0:
        print("No Medicines Found")

    else:
        print("\n-------------------------------------------------------------")
        print("ID\tName\tCategory\tQty\tPrice\tExpiry")
        print("-------------------------------------------------------------")

        print("-"*80)

        for row in data:

            print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}")

            if row[3] < 10:
                print("   LOW STOCK! Only", row[3], "units left.")


def search_medicine():

    try:
        mid = int(input("Enter Medicine ID : "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    cursor.execute(
        "SELECT * FROM medicine WHERE medicine_id=%s",
        (mid,)
    )

    data = cursor.fetchone()

    if data:

        print("\nMedicine Found")
        print("---------------------------")
        print("Medicine ID :", data[0])
        print("Medicine Name :", data[1])
        print("Category :", data[2])
        print("Quantity :", data[3])
        print("Price :", data[4])
        print("Expiry Date :", data[5])

    else:
        print("Medicine Not Found")


def update_medicine():

    try:
        mid = int(input("Enter Medicine ID : "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    cursor.execute("SELECT * FROM medicine WHERE medicine_id=%s", (mid,))
    data = cursor.fetchone()

    if data:

        try:
            quantity = int(input("Enter New Quantity : "))
            price = float(input("Enter New Price : "))
        except ValueError:
            print("Invalid quantity or price. Please enter numbers only.")
            return

        cursor.execute(
            "UPDATE medicine SET quantity=%s, price=%s WHERE medicine_id=%s",
            (quantity, price, mid)
        )

        conn.commit()

        print("Medicine Updated Successfully")

    else:

        print("Medicine Not Found")


def delete_medicine():

    try:
        mid = int(input("Enter Medicine ID : "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    cursor.execute("SELECT * FROM medicine WHERE medicine_id=%s", (mid,))
    data = cursor.fetchone()

    if data:

        cursor.execute(
            "DELETE FROM medicine WHERE medicine_id=%s",
            (mid,)
        )

        conn.commit()

        print("Medicine Deleted Successfully")

    else:

        print("Medicine Not Found")


def add_to_cart():

    try:
        mid = int(input("Enter Medicine ID : "))
        qty = int(input("Enter Quantity : "))
    except ValueError:
        print("Invalid ID or quantity. Please enter numbers only.")
        return

    cursor.execute("SELECT * FROM medicine WHERE medicine_id=%s", (mid,))
    data = cursor.fetchone()

    if data:

        if qty <= 0:
            print("Quantity must be greater than 0.")

        elif qty > data[3]:
            print("Insufficient Stock")

        else:

            total = qty * float(data[4])

            cart.append({
                "id": data[0],
                "name": data[1],
                "price": float(data[4]),
                "quantity": qty,
                "total": total
            })

            print("Product Added To Cart")

    else:

        print("Medicine Not Found")


def remove_from_cart():

    try:
        mid = int(input("Enter Medicine ID To Remove : "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    for item in cart:

        if item["id"] == mid:

            cart.remove(item)

            print("Product Removed Successfully")

            return

    print("Product Not Found In Cart")


def view_cart():

    if len(cart) == 0:

        print("Cart Is Empty")

    else:

        grand_total = 0

        print("\n---------------------------------------------------------")
        print("ID\tName\tQty\tPrice\tTotal")
        print("---------------------------------------------------------")

        for item in cart:

            print(item["id"], "\t", item["name"], "\t", item["quantity"], "\t", item["price"], "\t", item["total"])

            grand_total += item["total"]

        print("---------------------------------------------------------")
        print("Grand Total :", grand_total)


def clear_cart():
    cart.clear()
    print("Cart Cleared Successfully")


def generate_bill():

    global bill_data

    if len(cart) == 0:

        print("Cart Is Empty")
        return

    customer = input("Enter Customer Name : ").strip()

    if not customer:
        print("Customer name cannot be empty.")
        return

    grand_total = 0
    bill_items = []

    print("\n==========================================")
    print("        PHARMACY STORE BILL")
    print("==========================================")
    print("Customer :", customer)
    print("------------------------------------------")
    print("Medicine\tQty\tPrice\tTotal")

    for item in cart:

        print(item["name"], "\t", item["quantity"], "\t", item["price"], "\t", item["total"])

        grand_total += item["total"]
        bill_items.append(item)

        cursor.execute(
            "UPDATE medicine SET quantity = quantity - %s WHERE medicine_id=%s",
            (item["quantity"], item["id"])
        )

    conn.commit()

    gst = grand_total * 0.18
    final_amount = grand_total + gst

    print("------------------------------------------")
    print("Sub Total :", grand_total)
    print("GST (18%) :", gst)
    print("Final Amount :", final_amount)
    print("==========================================")

    bill_data = {
        "customer": customer,
        "items": bill_items,
        "subtotal": grand_total,
        "gst": gst,
        "final": final_amount
    }

    cart.clear()

    print("Bill Generated Successfully")

    


def create_pdf():

    if bill_data is None:
        print("No bill has been generated yet. Use option 10 first.")
        return

    pdf = canvas.Canvas("Bill.pdf", pagesize=A4)
    width, height = A4

    y = height - 60

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2, y, "PHARMACY STORE BILL")
    y -= 40

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Customer: {bill_data['customer']}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Name")
    pdf.drawString(250, y, "Qty")
    pdf.drawString(320, y, "Price")
    pdf.drawString(420, y, "Total")
    y -= 15
    pdf.line(50, y, width - 50, y)
    y -= 20

    pdf.setFont("Helvetica", 11)
    for item in bill_data["items"]:
        pdf.drawString(50, y, str(item["name"]))
        pdf.drawString(250, y, str(item["quantity"]))
        pdf.drawString(320, y, f"{item['price']:.2f}")
        pdf.drawString(420, y, f"{item['total']:.2f}")
        y -= 20

        if y < 80:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = height - 60

    y -= 10
    pdf.line(50, y, width - 50, y)
    y -= 25

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, f"Subtotal: {bill_data['subtotal']:.2f}")
    y -= 20
    pdf.drawString(50, y, f"GST (18%): {bill_data['gst']:.2f}")
    y -= 20
    pdf.drawString(50, y, f"Final Amount: {bill_data['final']:.2f}")
    y -= 40

    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawString(50, y, "Thank You For Shopping!")

    pdf.save()

    print("PDF Created Successfully")

    receiver = input("Enter Receiver Gmail: ")
    sender = "hiteshj2900@gmail.com"
    app_password = "zzsgbkzpypmzfkax"

    msg = EmailMessage()

    msg["Subject"] = "Pharmacy bill PDF"
    msg["From"] = sender
    msg["To"] = receiver

    msg.set_content("Please find the attached Pharmacy Bill PDF.")

    with open("Bill.pdf", "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename("Bill.pdf")
        )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, app_password)
            smtp.send_message(msg)

        print("PDF Sent Successfully!")

    except Exception as e:
        print("Error:", e)


def sale_menu():
    while True:
        print("\n===== PHARMACY STORE MANAGEMENT =====")
        print("1. Add Medicine")
        print("2. View Medicines")
        print("3. Search Medicine")
        print("4. Update Medicine")
        print("5. Delete Medicine")
        print("6. Add To Cart")
        print("7. Remove From Cart")
        print("8. View Cart")
        print("9. Clear Cart")
        print("10. Generate Bill")
        print("11. Create PDF")
        print("12. Exit")

        try:
            choice = int(input("Enter Your Choice: "))
        except ValueError:
            print("Invalid Choice! Please enter a number between 1 and 12.")
            continue

        if choice == 1:
            add_medicine()

        elif choice == 2:
            view_medicines()

        elif choice == 3:
            search_medicine()

        elif choice == 4:
            update_medicine()

        elif choice == 5:
            delete_medicine()

        elif choice == 6:
            add_to_cart()

        elif choice == 7:
            remove_from_cart()

        elif choice == 8:
            view_cart()

        elif choice == 9:
            clear_cart()

        elif choice == 10:
            generate_bill()

        elif choice == 11:
            create_pdf()

        elif choice == 12:
            print("Thank You!")
            break

        else:
            print("Invalid Choice!")


