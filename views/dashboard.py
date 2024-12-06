import streamlit as st
from views.take_assessment import take_assessment
from views.view_assessment import view_assessment


def dashboard():
    # Initialize session state for the page if not already set
    if "page" not in st.session_state:
        st.session_state["page"] = "dashboard"  # Default to dashboard

    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        st.info("Explore your options:")

        # Persistent navigation using a radio button
        selected_page = st.radio(
            "Navigate to:",
            options=["Dashboard","Profile", "Take Assessment", "View Assessments", "Logout"],
            index=0 if st.session_state["page"] == "dashboard" else
                  1 if st.session_state["page"] == "profile" else
                  2 if st.session_state["page"] == "take_assessment" else
                  3 if st.session_state["page"] == "view_assessment" else 4,
        )

        # Update the page based on user selection
        if selected_page == "Dashboard":
            st.session_state["page"] = "dashboard"
        elif selected_page == "Take Assessment":
            st.session_state["page"] = "take_assessment"
            st.rerun()
        elif selected_page == "View Assessments":
            st.session_state["page"] = "view_assessment"
            st.rerun()
        elif selected_page == "Profile":
            st.session_state["page"] = "profile"
            st.rerun()
        elif selected_page == "Logout":
            # Clear session state and navigate to login page
            #st.session_state.clear()
            st.session_state["page"] = "login"
            st.rerun()
        

    # Render content based on the current page
    render_dashboard_content()



def render_dashboard_content():
    # Main dashboard content
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
        }
        .sub-header {
            font-size: 18px;
            color: #777;
            text-align: center;
        }
        .quote {
            font-style: italic;
            font-size: 20px;
            text-align: center;
            color: #555;
        }
        .quote-author {
            text-align: center;
            color: #888;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown("<div class='main-header'>Welcome to Your Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Track your mental health progress and take control of your well-being.</div>", unsafe_allow_html=True)

    # Motivational Quote
    st.markdown("<div class='quote'>\"The greatest wealth is health.\"</div>", unsafe_allow_html=True)
    st.markdown("<div class='quote-author'>- Virgil</div>", unsafe_allow_html=True)

    # Summary section
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Assessments Taken", value="15")  # Replace with actual data
    with col2:
        st.metric(label="Current Mood Trend", value="Positive")  # Replace with actual data
    with col3:
        st.metric(label="Longest Streak", value="5 Weeks")  # Replace with actual data

    # Additional Insights
    st.subheader("Quick Tips for a Healthy Mind:")
    st.write(
        """
        - Take deep breaths and practice mindfulness daily.
        - Stay connected with loved ones and share your feelings.
        - Engage in physical activities like yoga or walking.
        - Make sure to get enough sleep and eat a balanced diet.
        """
    )

    # Footer
    st.markdown(
        """
        <div style='text-align: center; margin-top: 50px; font-size: 14px; color: #777;'>
        Made with ❤️ using Streamlit | <a href="https://example.com/privacy" target="_blank">Privacy Policy</a> | <a href="https://example.com/terms" target="_blank">Terms of Use</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    dashboard()
