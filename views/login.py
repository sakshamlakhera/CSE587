import streamlit as st
from utils.database import login_user, create_usertable
from utils.auth import hash_password

def login():
    st.subheader("Login to Your Account")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if username == "" or password == "":
            st.error("Please provide both username and password.")
        else:
            create_usertable()
            hashed_password = hash_password(password)
            result = login_user(username, hashed_password)
            if result:
                st.success(f"Welcome {username}!")
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['page'] = "dashboard"  # Navigate to dashboard
                st.rerun()
            else:
                st.error("Incorrect username or password.")
        
