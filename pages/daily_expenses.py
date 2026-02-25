import streamlit as st
import sys
import os

# 1. HARDCODED path to your hackathon project root
# This tells Python EXACTLY where to look on your laptop
hackathon_root = r"C:\Users\91979\OneDrive\Desktop\hackathon\hackathon_project"

if hackathon_root not in sys.path:
    sys.path.insert(0, hackathon_root)

# 2. Try the import again
try:
    import expenses_db
    # We call it using the module name to be 100% safe
    expenses_db.init_db()
    
    # Alias the functions so your existing code doesn't break
    insert_expense = expenses_db.insert_expense
    get_categories = expenses_db.get_categories
    init_db = expenses_db.init_db
    
    st.success("Database connected successfully!")
except Exception as e:
    st.error(f"Critical Error: Could not find expenses_db.py in {hackathon_root}")
    st.info("Make sure the file 'expenses_db.py' is sitting directly in the 'hackathon_project' folder.")
    st.stop() # Stop the app here so we don't get the NameError below

st.title("Daily Expenses")

# Example Usage
categories = get_categories()
cat_options = {name: id for id, name in categories}
selected_cat_name = st.selectbox("Category", options=list(cat_options.keys()))

amount = st.number_input("Amount", min_value=0.0)
note = st.text_input("Note")
expense_date = st.date_input("Date")

if st.button("Add Expense"):
    insert_expense(amount, cat_options[selected_cat_name], str(expense_date), note)
    st.success("Expense added!")