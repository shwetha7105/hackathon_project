import streamlit as st
import sqlite3
import os
from datetime import date
import pandas as pd

# --- 1. SETUP DATABASE PATH ---
# This ensures the DB is in the 'hackathon_project' folder, not the 'pages' folder.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
DB_PATH = os.path.join(parent_dir, "expenses.db")

# --- 2. DATABASE FUNCTIONS ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category_id INTEGER,
            date TEXT NOT NULL,
            note TEXT,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    """)
    # Seed default categories if the table is empty
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        cats = [('Food',), ('Transport',), ('Entertainment',), ('Shopping',), ('Bills',)]
        cursor.executemany("INSERT INTO categories (category_name) VALUES (?)", cats)
    conn.commit()
    conn.close()

def get_categories():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, category_name FROM categories ORDER BY category_name")
    data = cursor.fetchall()
    conn.close()
    return data

def insert_expense(amount, cat_id, exp_date, note):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (amount, category_id, date, note)
        VALUES (?, ?, ?, ?)
    """, (amount, cat_id, str(exp_date), note))
    conn.commit()
    conn.close()

# --- 3. STREAMLIT UI ---
init_db()  # This runs every time the page refreshes to ensure tables exist

st.title("💸 Daily Expenses Tracker")

# Fetch data for the dropdown
try:
    categories = get_categories()
    cat_options = {name: id for id, name in categories}

    # Input Form
    with st.form("expense_form", clear_on_submit=True):
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        selected_cat = st.selectbox("Category", options=list(cat_options.keys()))
        exp_date = st.date_input("Date", value=date.today())
        note = st.text_input("Note (Optional)")
        
        submit = st.form_submit_button("Add Expense")
        
        if submit:
            if amount > 0:
                insert_expense(amount, cat_options[selected_cat], exp_date, note)
                st.success(f"Successfully added ₹{amount} to {selected_cat}!")
                st.rerun() # Refresh to show new data in the table
            else:
                st.error("Please enter an amount greater than zero.")
except Exception as e:
    st.error(f"UI Error: {e}")

# --- 4. DATA DISPLAY ---
st.divider()
st.subheader("Recent Expenses")

try:
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT e.amount, c.category_name as Category, e.date as Date, e.note as Note 
        FROM expenses e 
        JOIN categories c ON e.category_id = c.id 
        ORDER BY e.date DESC, e.id DESC LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No expenses recorded yet. Add one above!")
except Exception:
    st.info("Database initialized. Please add your first expense.")