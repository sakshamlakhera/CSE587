import streamlit as st
import sqlite3
import json
import hashlib

# Database connection
def connect_db():
    return sqlite3.connect('data.db', check_same_thread=False)

# Fetch user details
def fetch_user_details(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT details FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0]:
        return json.loads(result[0])  # Convert JSON string to dict
    return None

# Update user details
def update_user_details(username, details):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET details = ? WHERE username = ?", (json.dumps(details), username))
    conn.commit()
    conn.close()

# Update password
def update_password(username, new_password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    conn.close()

# Profile Section
def profile_section():
    # Sidebar Navigation
    with st.sidebar:
        st.title("Navigation")
        st.info("Explore your options:")

        selected_page = st.radio(
            "Navigate to:",
            options=["Dashboard","Profile", "Take Assessment", "View Assessments", "Logout"],
            index=0 if st.session_state.get("page") == "dashboard" else
                  1 if st.session_state.get("page") == "profile" else
                  2 if st.session_state.get("page") == "take_assessment" else
                  3 if st.session_state.get("page") == "view_assessment" else 4,
        )

        if selected_page == "Dashboard":
            st.session_state["page"] = "dashboard"
            st.rerun()
        elif selected_page == "Take Assessment":
            st.session_state["page"] = "take_assessment"
            st.rerun()
        elif selected_page == "View Assessments":
            st.session_state["page"] = "view_assessment"
            st.rerun()
        elif selected_page == "Profile":
            st.session_state["page"] = "profile"
        elif selected_page == "Logout":
            st.session_state["page"] = "login"
            st.rerun()

    # Header
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 32px;
            font-weight: bold;
            color: #4CAF50;
        }
        .sub-header {
            font-size: 18px; color: #777;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    username = st.session_state.get("username")  # Assuming username is stored in session
    st.markdown(f"<div class='main-header'>{username}'s Profile</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Manage your personal information here.</div>", unsafe_allow_html=True)

    # Fetch profile details from database
    user_details = fetch_user_details(username)

    if not user_details:
        user_details = {
            "first_name": "",
            "last_name": "",
            "age": 0,
            "is_gamer": False,
            "takes_intoxicants": False,
        }

    # Profile Form
    st.subheader("Edit Your Profile!")
    with st.form("profile_form", clear_on_submit=False):
        first_name = st.text_input("First Name", value=user_details.get("first_name", ""))
        last_name = st.text_input("Last Name", value=user_details.get("last_name", ""))
        age = st.number_input("Age", min_value=1, step=1, value=user_details.get("age", 0))
        is_gamer = st.checkbox("Are you a gamer?", value=user_details.get("is_gamer", False))
        print("users is ",user_details.get("takes_intoxicants"))
        takes_intoxicants = st.checkbox("Do you take intoxicants?", value=user_details.get("takes_intoxicants", False))

        # Save Button
        submitted = st.form_submit_button("Save")
        if submitted:
            # Update the profile in the database
            updated_details = {
                "first_name": first_name,
                "last_name": last_name,
                "age": age,
                "is_gamer": is_gamer,
                "takes_intoxicants": takes_intoxicants,
            }
            update_user_details(username, updated_details)
            st.success("Profile updated successfully!")
            st.session_state["current_question"] = 0

    # Password Change Form
    st.subheader("Change Your Password")
    with st.form("password_form", clear_on_submit=False):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        password_submitted = st.form_submit_button("Update Password")
        if password_submitted:
            if new_password != confirm_password:
                st.error("New password and confirmation do not match.")
            else:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()
                conn.close()
                hashed_current_password = hashlib.sha256(current_password.encode()).hexdigest()
                if result and result[0] == hashed_current_password:
                    update_password(username, new_password)
                    st.success("Password updated successfully!")
                else:
                    st.error("Current password is incorrect.")

    # Display Saved Profile
    st.subheader("Your Profile Information")
    st.write(f"**First Name:** {user_details.get('first_name', '')}")
    st.write(f"**Last Name:** {user_details.get('last_name', '')}")
    st.write(f"**Age:** {user_details.get('age', 0)}")
    st.write(f"**Gamer:** {'Yes' if user_details.get('is_gamer', False) else 'No'}")
    st.write(f"**Takes Intoxicants:** {'Yes' if user_details.get('takes_intoxicants', False) else 'No'}")

    # Footer
    st.markdown(
        """
        <div style='text-align: center; margin-top: 50px; font-size: 14px; color: #777;'>
        Made with ❤️
        </div>
        """,
        unsafe_allow_html=True,
    )
