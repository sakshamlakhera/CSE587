import re
import streamlit as st
from utils.database import add_userdata, create_usertable, login_user
from utils.auth import hash_password

def is_valid_email(email):
    """Validates the email format using a regular expression."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def signup():
    st.subheader("Create a New Account")
    
    # Basic user details
    new_user = st.text_input("Email Address")
    new_password = st.text_input("Password", type='password')

    # Additional user details
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    is_gamer = st.radio("Do you play games?", options=["Yes", "No"])
    takes_intoxicants = st.radio("Do you take intoxicants (e.g., drugs, cigarettes)?", options=["Yes", "No"])

    if st.button("Sign Up"):
        if new_user == "" or new_password == "":
            st.error("Please provide both email and password.")
        elif not is_valid_email(new_user):
            st.error("Please enter a valid email address.")
        elif first_name == "" or last_name == "":
            st.error("Please fill in all required fields.")
        else:
            create_usertable()
            hashed_new_password = hash_password(new_password)
            result = login_user(new_user, hashed_new_password)
            if result:
                st.error("An account with this email already exists.")
            else:
                # Prepare additional details in JSON format
                user_details = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "age": age,
                    "is_gamer": is_gamer,
                    "takes_intoxicants": takes_intoxicants
                }
                add_userdata(new_user, hashed_new_password, user_details)
                st.success("Account created successfully!")
                st.info("Go to the Login menu to log in.")
                st.session_state['current_page'] = 'login'  # Navigate to login
                st.rerun()
