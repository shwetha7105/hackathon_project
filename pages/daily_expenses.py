import streamlit as st
import sqlite3
from datetime import date

st.set_page_config(page_title="Daily Expenses", layout="centered")

st.title("Record Daily Expense")

# ----------------------------
# Database Connection
# ----------------------------
def get_connection():
    return sqlite3.connect("finance.db")

def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category_name FROM categories")
    data = cursor.fetchall()
    conn.close()
    return data

def insert_expense(amount, category_id, expense_date, note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (amount, category_id, date, note)
        VALUES (?, ?, ?, ?)
    """, (amount, category_id, expense_date, note))
    conn.commit()
    conn.close()

# ----------------------------
# Expense Form UI
# ----------------------------

with st.form("expense_form"):

    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("Enter Amount (₹)", min_value=0.0, step=1.0)

    with col2:
        expense_date = st.date_input("Select Date", value=date.today())

    categories = get_categories()

    if categories:
        category_dict = {name: id for id, name in categories}
        selected_category = st.selectbox("Select Category", list(category_dict.keys()))
    else:
        st.warning("No categories found. Please add categories first.")
        selected_category = None

    note = st.text_area("Add Note (Optional)")

    submit = st.form_submit_button("Add Expense")

# ----------------------------
# Submit Logic
# ----------------------------

if submit:
    if amount > 0 and selected_category:
        insert_expense(
            amount,
            category_dict[selected_category],
            expense_date.strftime("%Y-%m-%d"),
            note
        )
        st.success("✅ Expense Recorded Successfully!")
    else:
        st.error("Please enter valid details.")

        """
        reqired tables:

        
        CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category_id INTEGER,
    date TEXT,
    note TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
        """