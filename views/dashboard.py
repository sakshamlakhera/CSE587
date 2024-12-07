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

    # with col1:
    #     st.metric(label="Total Assessments Taken", value="15")  # Replace with actual data
    # with col2:
    #     st.metric(label="Current Mood Trend", value="Positive")  # Replace with actual data
    # with col3:
    #     st.metric(label="Longest Streak", value="5 Weeks")  # Replace with actual data

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

    st.markdown(
        """
        <style>
        .fact-header {
            font-size: 24px;
            font-weight: bold;
            color: #4A4A4A;
            text-align: center;
            text-decoration: underline;
        }
        </style>
        <div class='fact-header'>Our Analysis</div>
        """,
        unsafe_allow_html=True,
    )

    
    st.write(
        """
        #### Young Gamers and Anxiety:
        - Young gamers (18–25) experience higher anxiety levels.
        - Ages 18–20 & 21–25 feel afraid as if something awful might happen (GAD-7).
        - Ages 25–30 feel restless and find it hard to sit still (GAD-5).
        - Ages 30+ worry too much and can't stop/control worrying (GAD-2).
        """
    )

    st.write(
        """
        #### Parenting and Child Mental Health:
        - Praising children significantly reduces their depression levels.
        - Moderately limiting TV and playtime benefits mental health. Extreme restrictions may lead to depression.
        - Parental involvement in schoolwork positively affects children's happiness.
        - Frequent arguments or fights between parents and children increase depression risk.
        - Talking to children about the impacts of intoxicants slightly improves mental health.
        """
    )

    st.write(
        """
        #### Socio-Economic Status and Depression:
        - Individuals earning less than $20,000 are more likely to experience depression.
        - Wealthier individuals tend to report lower levels of depression.
        """
    )

    st.write(
        """
            #### Early drug use and its effects on mental health issues:
            - 83.4% of individuals who did not use drugs early are not depressed, while 16.6% are depressed.
            - In contrast, 65.6% of individuals who used drugs early are not depressed, but 34.4% suffer from depression.
            - The T-statistic (43.341) and P-value (0) strongly indicate a relationship between early drug use and mental health issues.
            - This suggests that early drug use could be a risk factor for depression, as the "Drug Use" group shows a significantly higher proportion of depression compared to the "No Drug Use" group.
        """
    )
    
    st.write(
        """
        #### Religious Belief and Mental Health:
        - Individuals with strong religious beliefs are less susceptible to suicidal thoughts.
        - People with "no belief" have the highest rates of suicidal thoughts.
        - Faith provides a sense of purpose, community, and hope, which combats feelings of despair.
        - Having religious beliefs offers protection against depression and suicidal ideation.
        """
    )

    st.write(
        """
        #### Insurance and Mental Health:
        - High-income individuals without insurance are more likely to be depressed than those with insurance.
        - Insurance provides a sense of safety and reduces stress about medical emergencies.
        - A high-income individual without insurance is more susceptible to mental health issues compared to their insured counterparts.
        - In conclusion, having insurance positively impacts mental health, especially for individuals with higher incomes.
        """
    )

    st.write(
        """
        #### Smoking and Depression:
        - Smoking is not a direct factor for depression but an indirect one influenced by societal, financial, and personal causes.
        - Low-income individuals are advised to avoid cigarette smoking as it can worsen mental health issues.
        - Withdrawal symptoms after quitting smoking are known to cause anxiety and depression.
        - For individuals who continue smoking, their societal and financial stress plays a larger role than smoking itself.
        """
    )
    # Footer
    st.markdown(
        """
        <div style='text-align: center; margin-top: 50px; font-size: 14px; color: #777;'>
        Made with ❤️ 
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    dashboard()
