import streamlit as st

st.write("REGISTRATION")
already_have_account=st.checkbox("Already have an account?")
if already_have_account:
   # st.markdown("<a href='app/pages/login.py' target='_self'>Go to Login Page</a>", unsafe_allow_html=True)
    st.write("Please go to the Login Page ")
else:
    name=st.text_input("Name")
    email=st.text_input("Email address")
    password=st.text_input("Password")
    st.button("Register")
