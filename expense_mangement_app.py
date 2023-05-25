import streamlit as st
import pymysql

import streamlit as st
import pymysql

# Establish MySQL connection
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="2668",
    database="expenseManagement"
)
cursor = conn.cursor()

# Create expenses table
create_expenses_table_query = '''
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    receipt BLOB,
    tagged_members VARCHAR(255)
)
'''

cursor.execute(create_expenses_table_query)
conn.commit()

# Create groups table
create_groups_table_query = '''
CREATE TABLE IF NOT EXISTS `groups` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(255) NOT NULL,
    group_purpose VARCHAR(255)
)
'''

cursor.execute(create_groups_table_query)
conn.commit()

# Home page
def home():
    st.write("Welcome to the Expense Management App")

# Rest of the code...


# Create a new expense
def create_expense():
    description = st.text_input("Description")
    amount = st.number_input("Amount")
    receipt = st.file_uploader("Receipt")
    tagged_members = st.multiselect("Tagged Members", ["A", "B", "C", "D", "E"])

    if st.button("Add Expense"):
        sql = "INSERT INTO expenses (description, amount, receipt, tagged_members) VALUES (%s, %s, %s, %s)"
        values = (description, amount, receipt, ",".join(tagged_members))
        cursor.execute(sql, values)
        conn.commit()
        st.success("Expense added successfully!")

# List all expenses
def list_expenses():
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    st.write("Expenses:")
    for expense in expenses:
        st.write(f"- Description: {expense[1]}, Amount: {expense[2]}")

# Create a new payment
def create_payment():
    sender = st.text_input("Sender")
    recipient = st.text_input("Recipient")
    amount = st.number_input("Amount")

    if st.button("Add Payment"):
        sql = "INSERT INTO payments (sender, recipient, amount) VALUES (%s, %s, %s)"
        values = (sender, recipient, amount)
        cursor.execute(sql, values)
        conn.commit()
        st.success("Payment added successfully!")

# List all payments
def list_payments():
    cursor.execute("SELECT * FROM payments")
    payments = cursor.fetchall()
    st.write("Payments:")
    for payment in payments:
        st.write(f"- Sender: {payment[1]}, Recipient: {payment[2]}, Amount: {payment[3]}")

# Create a new group
def create_group():
    group_name = st.text_input("Group Name")
    group_purpose = st.text_input("Group Purpose")

    if st.button("Create Group"):
        sql = "INSERT INTO groups (group_name, group_purpose) VALUES (%s, %s)"
        values = (group_name, group_purpose)
        cursor.execute(sql, values)
        conn.commit()
        st.success("Group created successfully!")

# List all groups
def list_groups():
    cursor.execute("SELECT * FROM groups")
    groups = cursor.fetchall()
    st.write("Groups:")
    for group in groups:
        st.write(f"- Group Name: {group[1]}, Group Purpose: {group[2]}")

# App navigation
def main():
    pages = {
        "Home": home,
        "Create Expense": create_expense,
        "List Expenses": list_expenses,
        "Create Payment": create_payment,
        "List Payments": list_payments,
        "Create Group": create_group,
        "List Groups": list_groups
    }

    st.sidebar.title("Expense Management App")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page()

if __name__ == '__main__':
    main()
