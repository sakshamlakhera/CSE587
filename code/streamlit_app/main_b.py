import streamlit as st
import sqlite3
import pandas as pd
from topsis import run_topsis  # Import custom TOPSIS module
from models import model1, model2, model3, model4  # ML Models

# Database Setup
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY,
            age INTEGER,
            games_play BOOLEAN,
            questions TEXT,
            answers TEXT
        )
    ''')
    conn.commit()
    return conn

# Save responses
def save_response(conn, age, games_play, questions, answers):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO responses (age, games_play, questions, answers)
        VALUES (?, ?, ?, ?)
    ''', (age, games_play, ','.join(questions), ','.join(map(str, answers))))
    conn.commit()

# Dynamic Question Tree
def dynamic_questions():
    questions = []
    answers = []

    age = st.number_input("What is your age?", min_value=1, max_value=120, step=1)
    questions.append("What is your age?")
    answers.append(age)

    if age < 18:
        play_games = st.radio("Do you play games?", ["Yes", "No"])
        questions.append("Do you play games?")
        answers.append(play_games)

        if play_games == "Yes":
            # Gaming Questions
            questions += ["What game do you play the most?", "How many hours do you play games each day?", "What is your country of residence?"]
            answers.append(st.text_input("What game do you play the most?"))
            answers.append(st.number_input("How many hours do you play games each day?", min_value=0, max_value=24, step=1))
            answers.append(st.text_input("What is your country of residence?"))
        else:
            # Kid-Specific Questions
            for question in [
                "Do you check your kid's homework?",
                "Do you help your kid with homework?",
                "Does your kid seem to have lost interest in playing or other activities?",
                "Do you make your kid do household chores?",
                "Do you limit your kid's TV watching time?",
                "Do you limit your kid's playtime?",
                "Does your kid feel discouraged while doing tasks?",
                "Do you say 'Good Job' to your kid when they do a good job?",
                "Do you let your kid know you are proud of them?",
                "Do you have fewer arguments or fights with your kid?",
                "Do you talk to your kid about the bad effects of drugs?"
            ]:
                questions.append(question)
                answers.append(st.radio(question, ["Yes", "No"]))

    elif 18 <= age <= 21:
        play_games = st.radio("Do you play games?", ["Yes", "No"])
        questions.append("Do you play games?")
        answers.append(play_games)

        if play_games == "Yes":
            # General + Gaming Questions
            for question in [
                "What is your employment status?",
                "What is your highest level of education?",
                "What is your income level?",
                "What is your sexual orientation?",
                "How often have you felt sad that nothing could cheer you up?",
                "Have you had several days or longer when you felt sad, empty, or depressed?",
                "What game do you play the most?",
                "How many hours do you play games each day?",
                "What is your country of residence?"
            ]:
                questions.append(question)
                answers.append(st.text_input(question) if "What" in question else st.radio(question, ["Yes", "No"]))

    else:
        substances = st.radio("Have you used substances in your lifetime?", ["Yes", "No"])
        questions.append("Have you used substances in your lifetime?")
        answers.append(substances)

        if substances == "Yes":
            # Substance Use + General Questions
            for question in [
                "What is your employment status?",
                "What is your highest level of education?",
                "What is your income level?",
                "What is your sexual orientation?",
                "How often have you felt sad that nothing could cheer you up?",
                "Have you had several days or longer when you felt sad, empty, or depressed?",
                "At what age did you first use Marijuana?",
                "At what age did you first use a Blunt?",
                "At what age did you first use Cocaine?",
                "At what age did you first use Crack Cocaine?",
                "At what age did you first use Heroin?",
                "At what age did you first use Hallucinogens (LSD, mushrooms, etc.)?",
                "At what age did you first use Methamphetamine?"
            ]:
                questions.append(question)
                answers.append(st.text_input(question) if "What" in question else st.number_input(question, min_value=0, step=1))

    return questions, answers

# ML Model Execution
def execute_models(answers):
    models = st.multiselect("Select models to execute:", ["Model 1", "Model 2", "Model 3", "Model 4"])
    results = {}
    for model in models:
        if model == "Model 1":
            results["Model 1"] = model1.predict(answers)
        elif model == "Model 2":
            results["Model 2"] = model2.predict(answers)
        elif model == "Model 3":
            results["Model 3"] = model3.predict(answers)
        elif model == "Model 4":
            results["Model 4"] = model4.predict(answers)
    return results

# MCDM using TOPSIS
def combine_results(results):
    if results:
        scores = run_topsis(results)
        st.write("Combined Score using TOPSIS:")
        st.write(scores)

# Main Streamlit Application
def main():
    st.title("Dynamic Questionnaire and Analysis")
    conn = init_db()

    st.header("Dynamic Question Tree")
    questions, answers = dynamic_questions()

    if st.button("Save Responses"):
        save_response(conn, answers[0], answers[1] if len(answers) > 1 else None, questions, answers)
        st.success("Responses saved successfully!")

    st.header("Run Models")
    results = execute_models(answers)

    st.header("MCDM Analysis")
    combine_results(results)

if __name__ == "__main__":
    main()
