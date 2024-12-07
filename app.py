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
    print("selcted action is",selected_action )
    # Layout with two columns
    col1, col2 = st.columns([3, 2])

    with col1:
        # Left side: Project details
        st.title("Welcome to the Mental Health Assessment App")
        st.subheader("About the Project")
        st.markdown(
            """
            <p style="font-size:16px; line-height:1.5;">
                <p>
                The Depression Assessment App is designed to support individuals in taking an active role in their mental health
                journey. With this user-friendly app, you can easily track your emotional well-being, identify patterns or trends, 
                and determine if seeking professional help might be the right step for you.
            </p>

            <div class="feature-section">
                <h2>What This App Offers:</h2>
                <ul>
                    <li>Comprehensive Assessments: Take control of your mental health with thoughtfully designed assessments. Gain valuable insights and discover strategies to help you navigate and overcome challenges.</li>
                    <li>Progress Tracking: Keep track of your journey by reviewing past assessments. Identify trends and measure your progress over time to stay informed and empowered.</li>
                    <li>Secure Data: Your data is securely stored and remains confidential.</li>
                </ul>
            </div>
            
            <h2 style="color:#6c63ff;">Features:</h2>
            <ul>
                <li>Take assessments to understand your mental health.</li>
                <li>View past assessments and track progress.</li>
                <li>Data is securely stored and confidential.</li>
            </ul>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.header("Access Your Account")
        # Radio button to toggle between Login and Sign Up

        action = st.radio("Choose an action:", ["Login", "Sign Up"])
        
        if action == "Login":
            st.session_state['page'] = 'login'
            login()
        elif action == "Sign Up":
            signup()

if __name__ == '__main__':
    createQuestion()
    createDB()
    main()

    
