import streamlit as st
import pandas as pd
import altair as alt
from utils.database import get_assessments


def interpret_anxiety(score):
    if score <= 4:
        return "Minimal Anxiety", "😊"
    elif score <= 9:
        return "Mild Anxiety", "🙂"
    elif score <= 14:
        return "Moderate Anxiety", "😐"
    else:
        return "Severe Anxiety", "😟"

def interpret_satisfaction(score):
    if score >= 31:
        return "Extremely Satisfied with life", "😄"
    elif score >= 26:
        return "Satisfied with life", "🙂"
    elif score >= 20:
        return "Neutral or Slightly Satisfied with life", "😐"
    elif score >= 15:
        return "Slightly Dissatisfied with life", "😕"
    elif score >= 10:
        return "Dissatisfied with life", "😟"
    else:
        return "Extremely Dissatisfied with life", "😢"
    
def interpret_social_phobia(score):
    if score <= 20:
        return "No Social Phobia", "😊"
    elif score <= 30:
        return "Mild Social Phobia", "🙂"
    elif score <= 40:
        return "Moderate Social Phobia","😐"
    elif score <= 50:
        return "Severe Social Phobia", "😐"
    else:
        return "Very Severe Social Phobia", "😟"

def interpret_mental_heath(score):
    if score == 0:
        return "Low Probability of mental health issues", "😄"
    else:
        return "High Probability of mental health issues", "😢"
    
def interpret_depressive_episode(score):
    if score == 0:
        return "Low Probability of severe Depressive Episode", "😄"
    else:
        return "High Probability of severe Depressive Episode", "😢"

def interpret_total(score):
    if score <= 20:
        return "You are Super Healthy", "🧗‍♂️"
    elif score <= 40:
        return "Pleae take Care of your Mental Health", "🙍‍♂️"
    elif score <= 60:
        return "Please Visit your local Doctor", "😟"
    else:
        return "Please get Consultation ASAP", "😟"

def view_assessment():
    # Sidebar Navigation
    with st.sidebar:
        st.title("Navigation")
        st.info("Explore your options:")

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
            st.rerun()
        elif selected_page == "Take Assessment":
            st.session_state["page"] = "take_assessment"
            st.rerun()
        elif selected_page == "View Assessments":
            st.session_state["page"] = "view_assessment"
        elif selected_page == "Profile":
            st.session_state["page"] = "profile"
            st.rerun()
        elif selected_page == "Logout":
            # Clear session state and navigate to login page
            #st.session_state.clear()
            st.session_state["page"] = "login"
            st.rerun()

    st.markdown(
        """
        <style>
        .main-header {
            font-size: 32px; font-weight: bold; color: #4CAF50;
        }
        .sub-header {
            font-size: 18px; color: #777;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='main-header'>Assessment Insights</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Explore your mental health trends and detailed insights.</div>", unsafe_allow_html=True)

    # Fetch assessments from the database
    assessments = get_assessments(st.session_state["username"])

    if assessments.empty:
        st.info("You have not taken any assessments yet.")
        return

    # Process the data
    assessments["date"] = pd.to_datetime(assessments["date"])
    assessments = assessments.sort_values("date").reset_index(drop=True)
    assessments["iteration"] = assessments.index + 1

    # Calculate total score as average of the 5 metrics
    metrics = ["anxiety", "satisfaction", "social_phobia", "mental_health", "depressive_episode"]
    assessments["total_score"] = assessments[metrics].mean(axis=1)

    # Trend Visualization (Iteration-wise)
    st.subheader("Trend Visualization")
    # Create a selection for interactive filtering
    selection = alt.selection_multi(fields=["variable"], bind="legend")

    # Melt the DataFrame for Altair
    melted_data = assessments.melt(id_vars=["iteration"], value_vars=metrics)

    # Create the interactive trend chart
    trend_chart = (
        alt.Chart(melted_data, title="Metric Trends by Iteration")
        .mark_line(point=True)
        .encode(
            x=alt.X("iteration:O", title="Iteration"),
            y=alt.Y("value:Q", title="Score"),
            color=alt.Color("variable:N", title="Metric"),
            tooltip=["iteration:O", "variable:N", "value:Q"],
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
        )
        .add_selection(selection)
        .properties(width="container", height=400)
    )

    # Display the chart
    st.altair_chart(trend_chart, use_container_width=True)

    # 10-iteration average
    if len(assessments) >= 10:
        st.subheader("10-Iteration Average")
        avg_data = assessments.tail(10).mean()
        avg_df = avg_data[metrics].reset_index()
        avg_df.columns = ["Metric", "Average Score (%)"]
        st.table(avg_df)

    # Dropdown to view reports
    st.sidebar.markdown("### View Reports")
    dropdown_options = ["Latest"] + assessments["iteration"].tolist()
    selected_iteration = st.sidebar.selectbox(
        "Select an Iteration:",
        options=dropdown_options,
        format_func=lambda x: f"Iteration {x}" if isinstance(x, int) else x
    )

    # Display the selected report
    if selected_iteration == "Latest":
        selected_report = assessments.iloc[-1]
        st.subheader("Report for Latest Iteration")
    else:
        selected_report = assessments[assessments["iteration"] == selected_iteration].iloc[0]
        st.subheader(f"Report for Iteration {selected_iteration}")

    # Display metrics in 2x4 format
    total_score_string, total_score_emoji = interpret_total(selected_report['total_score'])
    st.metric(total_score_string, total_score_emoji)

    cols = st.columns(3)
    anxiety_string, anxiety_emoji =interpret_anxiety(selected_report['anxiety'])
    satisfaction_string, satisfaction_emoji =  interpret_satisfaction(selected_report['satisfaction'])
    social_phobia_string, social_phobia_string_emoji =  interpret_social_phobia(selected_report['social_phobia'])
    mental_health_string, mental_health_string_emoji = interpret_mental_heath(selected_report['mental_health'])
    depressive_episode_string, depressive_episode_emoji = interpret_depressive_episode(selected_report['depressive_episode'])

    cols[0].metric(anxiety_string, f"{selected_report['anxiety']}/21 {anxiety_emoji}")
    cols[1].metric(satisfaction_string, f"{selected_report['satisfaction']}/35 {satisfaction_emoji}")
    cols[2].metric(social_phobia_string, f"{selected_report['social_phobia']}/68 {social_phobia_string_emoji}")

    cols = st.columns(2)
    cols[0].metric(mental_health_string, mental_health_string_emoji)
    cols[1].metric(depressive_episode_string, depressive_episode_emoji)


    st.subheader("Summary of All Iterations")
    st.dataframe(assessments[["iteration", "date", "total_score"] + metrics])

    # Export option
    st.download_button(
        label="Download Assessment History",
        data=assessments.to_csv(index=False),
        file_name="assessment_history.csv",
        mime="text/csv"
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
