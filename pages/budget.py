import streamlit as st
import sqlite3


def init_tables():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Create budgets table  
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            budget_amount REAL,
            month TEXT
        )
    ''')
    
    # Add sample categories if empty
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        categories = [('Food',), ('Transport',), ('Shopping',), ('Bills',), ('Entertainment',)]
        cursor.executemany("INSERT INTO categories (category_name) VALUES (?)", categories)
        st.success("✅ Added sample categories!")
    
    conn.commit()
    conn.close()

init_tables()

st.write("BUDGET")
st.text_input("MonthlyIncome")
st.text_input("Monthly Budget")
st.button("Fix Budget")

def add_category(category_name):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (category_name,))
        conn.commit()
        st.success("Category added successfully!")
    except:
        st.warning("Category already exists!")
    conn.close()

st.title("Add New Category")
new_category = st.text_input("Enter Category Name")

if st.button("Add Category"):
    if new_category:
        add_category(new_category)

def get_categories():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, category_name FROM categories")
    data = cursor.fetchall()
    conn.close()
    return data

st.subheader("Set Budget")
categories = get_categories()

if categories:
    category_dict = {name: id for id, name in categories}
    selected_category = st.selectbox("Select Category", list(category_dict.keys()))
    budget_amount = st.number_input("Enter Budget Amount", min_value=0.0)
    month = st.text_input("Enter Month (YYYY-MM)")

    if st.button("Set Budget"):
        conn = sqlite3.connect("finance.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO budgets (category_id, budget_amount, month)
            VALUES (?, ?, ?)
        """, (category_dict[selected_category], budget_amount, month))
        conn.commit()
        conn.close()
        st.success("Budget Set Successfully!")
else:
    st.info("Please add categories first.")
