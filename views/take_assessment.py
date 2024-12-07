import streamlit as st
import sqlite3
from utils.database import add_assessment
import time
import json
from utils.database import get_questions_from_db, fetch_user_details
from utils.utils import tarsformForModel
import pandas as pd
from code.streamlit_app.core.modelmanager import ModelManager

def performQuestionSelection(user_details):
    models_needed = []
    #print("details is", user_details)
    age = user_details['age']
    is_gamer = user_details['is_gamer']
    takes_intoxicants = user_details['takes_intoxicants']
    question_arr = []
    if age <= 25 :
        if is_gamer:
            #print("gamer is",is_gamer)
            question_arr.append('Gaming')#apurva model
            models_needed.append("gmh_model")
        if age < 18:
            if takes_intoxicants:
                question_arr.append('Substance Use')# sharan, drug abuse
                models_needed.append("youth_drug_abuse_model")
        question_arr.append('Kid-Specific')#saksham model, all append please
        models_needed.append("child_behavioral_model")
    else:
        question_arr.append('General')
        models_needed.append("general_model")

    return question_arr, models_needed

def take_assessment():
    # Sidebar for navigation
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

        if selected_page == "Dashboard":
            st.session_state["page"] = "dashboard"
            st.rerun()
        elif selected_page == "Take Assessment":
            st.session_state["page"] = "take_assessment"
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
            font-size: 18px;
            color: #777;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='main-header'>Take Your Assessment</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Answer the questions to evaluate your responses.</div>", unsafe_allow_html=True)
    username = st.session_state.get("username", "default_user")  # Replace with actual username
    user_details = fetch_user_details(username)
    question_selection, models_needed = performQuestionSelection(user_details)
    #print(question_selection)
    # Fetch questions from the database
    

    # Initialize session state for responses and question index
    if "responses" not in st.session_state:
        st.session_state["responses"] = {}
    if "current_question" not in st.session_state:
        st.session_state["current_question"] = 0
    
    current_index = st.session_state["current_question"]
    print(current_index)
    questions = get_questions_from_db(question_selection)

    # Get the current question
    print(current_index)
    

    question = questions[current_index]['question']
    description = questions[current_index]['description']
    answer_type = questions[current_index]['answer_type']
    options = None
    if questions[current_index].get('options'):
        options = questions[current_index]['options']


    # Display the current question
    st.write(f"**Question {current_index + 1} of {len(questions)}:** {question}")
    

    # Handle options or text input
    input_value = None
    model_map = 0
    if answer_type == 'radio':
        display_options = [option for option in options if option is not None]
        input_value = st.radio(
            "Your Answer:",
            options=display_options
        )
        model_map = options.index(input_value)
    elif answer_type =='text':
        # Handle text input with range validation
        input_value = st.number_input(
            "Enter your answer (0-100):", min_value=0, max_value=100, step=1, value=st.session_state.get("response", 0) 
        )
        model_map = input_value
    else:
        display_options = [option for option in options if option is not None]
        input_value = st.selectbox(
                "Your Answer:",
                options=display_options
            )
        model_map = options.index(input_value)
    
    st.session_state[f"response_{current_index}"] = (questions[current_index]['code'],input_value,model_map)
    # Display the description below the question
    st.info(description)

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    if current_index > 0:
        if col1.button("Previous", key="previous_button"):
            st.session_state["current_question"] -= 1
            st.rerun()

    if current_index < len(questions) - 1:
        if col3.button("Next", key="next_button"):
            st.session_state["current_question"] += 1
            st.rerun()

    # Submit button
    if current_index == len(questions) - 1:
        if col2.button("Submit Assessment", key="submit_button"):
            # Collect responses
            responses = {questions[i]['question']: st.session_state[f"response_{i}"][1] for i in range(len(questions))}
            inputmodel = { st.session_state[f"response_{i}"][0]: st.session_state[f"response_{i}"][2] for i in range(len(questions))}
            inputmodel['Age'] = user_details['age']
            print("input is ",inputmodel)
            final_input_df = tarsformForModel(inputmodel)
     
            print(final_input_df)
            models = ModelManager("database.db")
            print(models_needed)
            total_score = 0
            mental_health=anxiety=social_phobia= 0
            satisfaction = depressive_episode = None

            for model_name in models_needed:
                if model_name == "child_behavioral_model":
                    depressive_episode = models.run_models(pd.DataFrame.from_dict(final_input_df), "child_behavioral_model")
                    print('depressive_episode',depressive_episode)
                    total_score = float(depressive_episode)+100/user_details['age']
                if model_name == 'general_model':
                    mental_health = models.run_models(pd.DataFrame.from_dict(final_input_df), "general_model")
                if model_name == 'youth_drug_abuse_model':
                    mental_health = models.run_models(pd.DataFrame.from_dict(final_input_df), "youth_drug_abuse_model")
                if model_name == 'gmh_model':
                    anxiety ,satisfaction,  social_phobia = models.run_models(pd.DataFrame.from_dict(final_input_df), "gmh_model")
                    print('gmh_model',[anxiety ,satisfaction,  social_phobia ])
            
            if satisfaction == None:
                satisfaction = 1
            if depressive_episode == None:
                depressive_episode = 1
            

            age_factor = max(0, min(1, (90 - user_details['age']) / 75)) # Normalized factor for age, more weight for younger people
            depressive_weight = 30 * (1 - depressive_episode) * age_factor  # Weight for depressive episodes
            mental_health_weight = 20 * mental_health * age_factor  # Weight for general mental health
            anxiety_weight = 15 * anxiety * age_factor  # Weight for anxiety
            social_phobia_weight = 15 * social_phobia * age_factor  # Weight for social phobia
            satisfaction_weight = 20 * (1 - satisfaction) * age_factor  # Satisfaction reduces score

            total_score = depressive_weight + mental_health_weight + anxiety_weight + social_phobia_weight + satisfaction_weight
            total_score = min(total_score,100)

            add_assessment(st.session_state["username"], 
                           responses, 
                           total_score=int(total_score), 
                           anxiety=int(anxiety*21), 
                           satisfaction = int(satisfaction*30 + 5),
                           social_phobia=int(social_phobia*68),
                           mental_health=int(mental_health*100),
                           depressive_episode=int((1-depressive_episode)*100))  # Adjust total_score as needed
            st.success("Your assessment has been submitted!")

            # Reset state and navigate to view assessments
            st.session_state["responses"] = {}
            with st.spinner("Loading..."):
                st.balloons()
                time.sleep(2)
            st.session_state["current_question"] = 0
            st.session_state["page"] = "view_assessment"
            st.rerun()

    # Footer
    st.markdown(
        """
        <div style='text-align: center; margin-top: 50px; font-size: 14px; color: #777;'>
        Made with ❤️
        </div>
        """,
        unsafe_allow_html=True,
    )
