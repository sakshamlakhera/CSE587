import streamlit as st
from utils.database import add_assessment, create_assessment_table

def assessment():
    st.subheader("Depression Assessment Questionnaire")

    q1 = st.radio("1. Little interest or pleasure in doing things?", ("Not at all", "Several days", "More than half the days", "Nearly every day"))
    q2 = st.radio("2. Feeling down, depressed, or hopeless?", ("Not at all", "Several days", "More than half the days", "Nearly every day"))
    q3 = st.radio("3. Trouble falling or staying asleep, or sleeping too much?", ("Not at all", "Several days", "More than half the days", "Nearly every day"))
    q4 = st.radio("4. Feeling tired or having little energy?", ("Not at all", "Several days", "More than half the days", "Nearly every day"))
    q5 = st.radio("5. Poor appetite or overeating?", ("Not at all", "Several days", "More than half the days", "Nearly every day"))

    if st.button("Submit Assessment"):
        responses = f"{q1},{q2},{q3},{q4},{q5}"
        create_assessment_table()
        add_assessment(st.session_state['username'], responses)
        st.success("Assessment submitted successfully!")
