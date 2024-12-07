import sqlite3
import pandas as pd
from datetime import datetime
import json

# Database connection
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

# Create users table
# def create_usertable():
#     c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)')
#     conn.commit()
def create_usertable():
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, 
            password TEXT, 
            details TEXT
        )
    ''')
    conn.commit()


# # Add user data
# def add_userdata(username, password):
#     c.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, password))
#     conn.commit()

def add_userdata(username, password, details):
    details_json = json.dumps(details)  # Convert details to JSON format
    c.execute('INSERT INTO users(username, password, details) VALUES (?, ?, ?)', (username, password, details_json))
    conn.commit()


# Login user
def login_user(username, password):
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    return c.fetchall()

def check_user(username):
    c.execute('SELECT * FROM users WHERE username = ?', (username, ))
    return c.fetchall()

# Create assessments table
def create_assessment_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            username TEXT, 
            date TEXT, 
            responses TEXT, 
            total_score INTEGER,
            anxiety INTEGER,
            satisfaction INTEGER,
            social_phobia INTEGER,
            mental_health INTEGER,
            depressive_episode INTEGER
        )
    ''')
    conn.commit()



# Add an assessment
def add_assessment(username, responses, total_score, anxiety = 0, satisfaction = 0, social_phobia = 0, mental_health = 0, depressive_episode = 0 ):
    create_assessment_table()
    c.execute('''
        INSERT INTO assessments (username, date, responses, total_score, anxiety, satisfaction, social_phobia, mental_health ,depressive_episode)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(responses), total_score, anxiety, satisfaction, social_phobia, mental_health, depressive_episode))
    conn.commit()

# Get all assessments for a user
    
def get_assessments(username):
    create_assessment_table()
    # Select all relevant columns from the database
    c.execute('''
        SELECT date, responses, total_score, anxiety, satisfaction, social_phobia, mental_health, depressive_episode 
        FROM assessments WHERE username = ?
    ''', (username,))
    rows = c.fetchall()

    if rows:
        # Convert the rows to a DataFrame
        df = pd.DataFrame(
            rows,
            columns=["date", "responses", "total_score", "anxiety", "satisfaction", "social_phobia", "mental_health","depressive_episode"]
        )
        df["date"] = pd.to_datetime(df["date"])  # Ensure dates are in datetime format
        df["responses"] = df["responses"].apply(eval)  # Convert string back to dictionary if necessary
        return df
    else:
        # Return an empty DataFrame with appropriate column names
        return pd.DataFrame(
            columns=["date", "responses", "total_score", "anxiety", "satisfaction", "social_phobia", "mental_health", "depressive_episode"]
        )


def get_questions_from_db(question_types):
    """
    Fetches questions from the SQLite database based on the list of question types.
    Parses the 'details' column as JSON, includes the 'code', and returns a list of question dictionaries.
    """
    if not isinstance(question_types, list):
        raise ValueError("question_types must be a list")

    conn = sqlite3.connect("data.db")  # Connect to the SQLite database
    cursor = conn.cursor()

    # Create a parameterized query to use the IN clause
    placeholders = ", ".join("?" for _ in question_types)
    query = f"""
        SELECT code, details
        FROM questions 
        WHERE type IN ({placeholders});
    """

    cursor.execute(query, question_types)
    rows = cursor.fetchall()
    conn.close()

    # Parse the rows into a usable format
    questions = []
    for row in rows:
        try:
            code, details_json = row
            details_dict = json.loads(details_json)  # Convert stringified JSON to Python dict
            details_dict["code"] = code  # Add the 'code' into the JSON object
            questions.append(details_dict)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e} for row: {row}")
    return questions



def fetch_user_details(username):
    """
    Fetches user details from the users table in the database.
    """
    conn = sqlite3.connect("data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT details FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0]:
        return json.loads(result[0])  # Parse the JSON string into a Python dictionary
    return {"age": None, "is_gamer": None, "takes_intoxicants": None}  # Default if no data exists
