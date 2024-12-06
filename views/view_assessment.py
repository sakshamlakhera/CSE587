import streamlit as st
import pandas as pd
import altair as alt
from utils.database import get_assessments


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
            y=alt.Y("value:Q", title="Score (%)"),
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
    st.metric("Total Score", f"{selected_report['total_score']:.2f}")

    cols = st.columns(4)
    cols[0].metric("Anxiety", f"{selected_report['anxiety']}%")
    cols[1].metric("Satisfaction", f"{selected_report['satisfaction']}%")
    cols[2].metric("Social Phobia", f"{selected_report['social_phobia']}%")
    cols[3].metric("Mental Health", f"{selected_report['mental_health']}%")

    cols = st.columns(4)
    cols[0].metric("Depressive Episode", f"{selected_report['depressive_episode']}%")

    # Summary Table
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
        Made with ❤️ using Streamlit | <a href="https://example.com/privacy" target="_blank">Privacy Policy</a> | <a href="https://example.com/terms" target="_blank">Terms of Use</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
