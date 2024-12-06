import streamlit as st
from views.login import login
from views.signup import signup
from views.dashboard import dashboard
from views.take_assessment import take_assessment
from views.view_assessment import view_assessment
from views.profile import profile_section
from utils.questions import createQuestion
from code.streamlit_app.core.modelsdb import createDB

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'  # Default page

    if st.session_state['page'] == 'dashboard':
        dashboard()
    elif st.session_state['page'] == 'take_assessment':
        take_assessment()
    elif st.session_state['page'] == 'view_assessment':
        view_assessment()
    elif st.session_state['page'] == 'profile':
        profile_section()
    elif st.session_state['page'] in ['login', 'signup']:
        home(st.session_state['page'])  # Pass the selected action to home
    else:
        home()

def home(selected_action="login"):
    # Layout with two columns
    col1, col2 = st.columns([3, 2])

    with col1:
        # Left side: Project details
        st.title("Welcome to the Depression Assessment App")
        st.subheader("About the Project")
        st.markdown(
            """
            <p style="font-size:16px; line-height:1.5;">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt 
                ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation 
                ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit 
                in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            </p>
            
            <h2 style="color:#6c63ff;">Features:</h2>
            <ul>
                <li>Take assessments to understand your mental health.</li>
                <li>View past assessments and track progress.</li>
                <li>Data is securely stored and confidential.</li>
            </ul>
            
            <h1 style="color:#4a4a4a;">Saksham</h1>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.header("Access Your Account")
        # Radio button to toggle between Login and Sign Up
        action = st.radio("Choose an action:", ["Login", "Sign Up"], index=0 if selected_action == "login" else 1)

        if action == "Login":
            st.session_state['page'] = 'login'
            login()
        elif action == "Sign Up":
            st.session_state['page'] = 'signup'
            signup()

if __name__ == '__main__':
    createQuestion()
    createDB()
    main()
