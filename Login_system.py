import mysql.connector
from database import conn, cursor
import random
import smtplib
from email.mime.text import MIMEText


cursor.execute("""
CREATE TABLE IF NOT EXISTS login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role ENUM('Admin','User') NOT NULL
);
""")

conn.commit()





def register():
    print("\n========== REGISTER ==========")

    username = input("Enter Username : ").strip()
    email = input("Enter Email : ").strip()

    while True:
        password = input("Enter Password : ")
        confirm = input("Confirm Password : ")

        if password == confirm:
            break
        else:
            print("Passwords do not match. Try again.")

    
    role = "User"

    sql = """
    INSERT INTO login(username,email,password,role)
    VALUES(%s,%s,%s,%s)
    """

    try:
        cursor.execute(sql, (username, email, password, role))
        conn.commit()
        print("\nRegistration Successful!")

    except mysql.connector.IntegrityError:
        print("\nUsername or Email already exists.")



def login():

    print("\n========== LOGIN ==========")

    username = input("Username : ").strip()
    password = input("Password : ").strip()

    cursor.execute("""
    SELECT username, role
    FROM login
    WHERE username=%s
    AND password=%s
    """, (username, password))

    user = cursor.fetchone()

    if user:
        print("\nLogin Successful!")
        return user[1]     

    print("\nInvalid Username or Password.")
    return None



def change_password():

    print("\n========== CHANGE PASSWORD ==========")

    username = input("Enter Username : ").strip()
    old_password = input("Enter Current Password : ").strip()

    cursor.execute("""
    SELECT *
    FROM login
    WHERE username=%s
    AND password=%s
    """, (username, old_password))

    user = cursor.fetchone()

    if user:

        while True:

            new_password = input("Enter New Password : ").strip()
            confirm_password = input("Confirm New Password : ").strip()

            if new_password != confirm_password:
                print("Passwords do not match.")
                continue

            if new_password == old_password:
                print("New password cannot be the same as the old password.")
                continue

            break

        cursor.execute("""
        UPDATE login
        SET password=%s
        WHERE username=%s
        """, (new_password, username))

        conn.commit()

        print("\nPassword Changed Successfully!")

    else:
        print("\nInvalid Username or Current Password.")

def send_otp(receiver_email, otp):

    subject = "Pharmacy Management System - Password Reset OTP"

    body = f"""
Hello,

Your OTP for password reset is: {otp}

This OTP is valid for one use only.

Do not share this OTP with anyone.

Regards,
Pharmacy Management System
"""

    SENDER_EMAIL = "hiteshj2900@gmail.com"
    APP_PASSWORD = "zzsgbkzpypmzfkax"
    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(SENDER_EMAIL, APP_PASSWORD)

        server.send_message(msg)

        server.quit()

        return True

    except Exception as e:
        print("\nUnable to send OTP.")
        print(e)
        return False
    
def forgot_password():

    print("\n========== FORGOT PASSWORD ==========")

    username = input("Enter Username : ").strip()
    email = input("Enter Registered Email : ").strip()

    cursor.execute("""
    SELECT *
    FROM login
    WHERE username=%s
    AND email=%s
    """, (username, email))

    user = cursor.fetchone()

    if not user:
        print("\nUsername and Email do not match.")
        return

    otp = random.randint(100000, 999999)

    sent = send_otp(email, otp)

    if not sent:
        return

    print("\nOTP has been sent to your email.")

    attempts = 3

    while attempts > 0:

        entered_otp = input("Enter OTP : ")

        if entered_otp == str(otp):

            while True:

                new_password = input("Enter New Password : ")
                confirm_password = input("Confirm New Password : ")

                if new_password != confirm_password:
                    print("Passwords do not match.")
                    continue

                break

            cursor.execute("""
            UPDATE login
            SET password=%s
            WHERE username=%s
            """, (new_password, username))

            conn.commit()

            print("\nPassword Reset Successfully.")
            return

        else:
            attempts -= 1

            if attempts > 0:
                print(f"Incorrect OTP. {attempts} attempt(s) remaining.")

    print("\nMaximum OTP attempts exceeded.")


# ---------------- LOGIN MENU ---------------- #

def login_menu():

    while True:

        print("\n========== PHARMACY MANAGEMENT SYSTEM ==========")
        print("1. Register")
        print("2. Login")
        print("3. Change Password")
        print("4. Forgot Password")
        print("5. Exit")

        try:
            choice = int(input("\nEnter Your Choice : "))

        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            register()

        elif choice == 2:
            role = login()

            if role:
                return role

        elif choice == 3:
            change_password()

        elif choice == 4:
            forgot_password()

        elif choice == 5:
            print("Thank You!")
            break

        else:
            print("Invalid Choice.")