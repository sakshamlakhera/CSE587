import sqlite3
import json

# Define questions with full mapping and added 'code' column
questions = questions = [ 

("General", " Employment", { 

"question": "What is your employment status?", 

"description": "Select your current employment status.", 

"answer_type": "radio", 

"options": ["Employed full time", "Unemployed", " Employed part time", " Other (incl. not in labor force)"] 

}), 

("General", " Education", { 

"question": "What is your highest level of education?", 

"description": "Select your highest educational qualification.", 

"answer_type": "radio", 

"options": ["College Degree", " primary education", " High School education"] 

}), 

("General", " Income", { 

"question": "What is your income level?", 

"description": "Select your income range.", 

"answer_type": "radio", 

"options": ["Less than $20,000", " $50,000 - $74,999", " $75,000 or more"] 

}), 

("General", " IRSEX", { 

"question": "What is your sexual orientation?", 

"description": "Select your sexual orientation.", 

"answer_type": "radio", 

"options": ["Heterosexual", "Homosexual", "Bisexual", "Other"] 

}), 

("General", "HOW OFTEN FELT SAD NOTHING COULD CHEER YOU UP", { 

"question": "How often have you felt sad that nothing could cheer you up?", 

"description": "Select the frequency that best applies to you.", 

"answer_type": "radio", 

"options": ["None of the time", " A little of the time", " Some of the time", " Most of the time", " All of the time"] 

}), 

("General", "sad_depressed", { 

"question": "Have you had several days or longer when you felt sad, empty, or depressed?", 

"description": "Select Yes or No.", 

"answer_type": "radio", 

"options": ["Yes", "No"] 

}), 
("General", "Metro_NonMetro", { 

"question": "Do you stay in a Metro City?", 

"description": "Select Yes or No.", 

"answer_type": "radio", 

"options": ["Yes", "No"] 

}), 

 

# Gaming Questions 

("Gaming", "Game", { 

"question": "What game do you play the most?", 

"description": "Enter the name of the game you play most.", 

"answer_type": "drop-down",
"options":  ['Counter Strike', 'Destiny', 'Diablo 3', 'Guild Wars 2',
       'Hearthstone', 'Heroes of the Storm', 'League of Legends', 'Other',
       'Skyrim', 'Starcraft 2', 'World of Warcraft']

}), 

("Gaming", "Hours", { 

"question": "How many hours do you play the game every week?", 

"description": "Enter approximate weekly gaming time.", 

"answer_type": "text",

"range": [0, 168] 

}), 

("Gaming", "Residence", { 

"question": "What is your country of residence?", 

"description": "Select the name of your country.", 

"answer_type": "drop-down" ,
"options": ['Albania', 'Algeria', 'Argentina', 'Australia', 'Austria',
       'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 'Belize', 'Bolivia',
       'Bosnia and Herzegovina', 'Brazil', 'Brunei', 'Bulgaria', 'Canada',
       'Chile', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cyprus',
       'Czech Republic', 'Denmark', 'Dominican Republic', 'Ecuador',
       'Egypt', 'El Salvador', 'Estonia', 'Faroe Islands', 'Fiji',
       'Finland', 'France', 'Georgia', 'Germany', 'Gibraltar ', 'Greece',
       'Grenada', 'Guadeloupe', 'Guatemala', 'Honduras', 'Hong Kong',
       'Hungary', 'Iceland', 'India', 'Indonesia', 'Ireland', 'Israel',
       'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait',
       'Latvia', 'Lebanon', 'Liechtenstein', 'Lithuania', 'Luxembourg',
       'Macedonia', 'Malaysia', 'Malta', 'Mexico', 'Moldova', 'Mongolia',
       'Montenegro', 'Morocco', 'Namibia', 'Netherlands', 'New Zealand ',
       'Nicaragua', 'Norway', 'Pakistan', 'Palestine', 'Panama', 'Peru',
       'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar',
       'Republic of Kosovo', 'Romania', 'Russia', 'Saudi Arabia',
       'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa',
       'South Korea', 'Spain', 'St Vincent', 'Sweden', 'Switzerland',
       'Syria', 'Taiwan', 'Thailand', 'Trinidad & Tobago', 'Tunisia',
       'Turkey', 'UAE', 'UK', 'USA', 'Ukraine', 'Unknown', 'Uruguay',
       'Venezuela', 'Vietnam']

}), 



# Substance Use Questions 

("Substance Use", "MJAGE", { 

"question": "At what age did you first use Marijuana?", 

"description": "Enter the age when you first used Marijuana. Enter zero if not done", 

"answer_type": "text", 

"range": [10, 100] 

}), 

("Substance Use", "BLNTAGE", { 

"question": "At what age did you first use a Blunt?", 

"description": "Enter the age when you first used a Blunt. Enter zero if not done", 

"answer_type": "text", 

"range": [10, 100] 

}), 

("Substance Use", "COCAGE", { 

"question": "At what age did you first use Cocaine?", 

"description": "Enter the age when you first used Cocaine. Enter zero if not done", 

"answer_type": "text", 

"range": [10, 100] 

}), 

("Substance Use", "CRKAGE", { 

"question": "At what age did you first use Crack Cocaine?", 

"description": "Enter the age when you first used Crack Cocaine. Enter zero if not done", 

"answer_type": "text", 

"range": [10, 100] 

}), 

("Substance Use", "HERAGE", { 

"question": "At what age did you first use Heroin?", 

"description": "Enter the age when you first used Heroin. Enter zero if not done", 

"answer_type": "text", 

"range": [10, 100] 

}), 

("Substance Use", "HERAGE", { 

"question": "At what age did you first use Hallucinogens (LSD, mushrooms, etc.)?", 

"description": "Enter the age when you first used Hallucinogens. Enter zero if not done", 

"answer_type": "text", 

"range": [10, 100] 

}), 

("Substance Use", "METHAMAGE", { 

"question": "At what age did you first use Methamphetamine?", 

"description": "Enter the age when you first used Methamphetamine. Enter zero if not done", 

"answer_type": "text", 

"range": [10, 100] 

}), 


 

# Kid-Specific Questions 

("Kid-Specific", "NEWRACE2", { 

"question": "What is your Race?", 

"description": "Select which applies", 

"answer_type": "drop-down", 

"options": [None, 'NonHisp White', 'NonHisp Black/Afr Am', 'NonHisp Native Am/AK Native', 'NonHisp Native HI/Other Pac Isl', 'NonHisp Asian', 'NonHisp more than one race']

}),


("Kid-Specific", "YEPCHKHW", { 

"question": "Does your parent/Guardian check your homework?", 

"description": "Select which applies", 

"answer_type": "radio", 

"options": [None, "Always", "Sometimes", "Seldom", "Never"] 

}), 

("Kid-Specific", "YEPHLPHW", { 

"question": "Does your parent/guardian help you with homework?", 

"description": "Select which applies", 

"answer_type": "radio", 

"options": [None, "Always", "Sometimes", "Seldom", "Never"] 

}), 

("Kid-Specific", "YO_MDEA2", { 

"question": "Have you lost interest in playing or other any other favourite activities?", 

"description": "Select Yes or No.", 

"answer_type": "radio", 

"options": [None, "Yes", "No"] 

}), 

("Kid-Specific", "YEPCHORE", { 

"question": "Does your parents make you do household chores?", 

"description": "Select which applies.", 

"answer_type": "radio", 

"options": [None, "Always", "Sometimes", "Seldom", "Never"] 

}), 

("Kid-Specific", "YEPLMTTV", { 

"question": "Have your parents limited your TV watching time in past few months?", 

"description": "Select which applies.", 

"answer_type": "radio", 

"options": [None, "Always", "Sometimes", "Seldom", "Never"] 

}), 

("Kid-Specific", "YEPLMTSN", { 

"question": "Have your parents limited your playtime in past few months?", 

"description": "Select which applies.", 

"answer_type": "radio", 

"options": [None, "Always", "Sometimes", "Seldom", "Never"] 

}), 

("Kid-Specific", "YO_MDEA1", { 

"question": "Have you been feeling discouraged while doing tasks, or you are scared to do task that you usually liked?", 

"description": "Select Yes or No.", 

"answer_type": "radio", 

"options": [None, "Yes", "No"] 

}), 

("Kid-Specific", "YEPGDJOB", { 

"question": "Does your parents appreciate you when you have done a good/great job?", 

"description": "Select which applies.", 

"answer_type": "radio", 

"options": [None, "Always", "Sometimes", "Seldom", "Never"] 

}), 

("Kid-Specific", "YEPPROUD", { 

"question": "Does your parents let you know that they are proud of you?", 

"description": " Select which applies.", 

"answer_type": "radio", 

"options": [None, "Always", "Sometimes", "Seldom", "Never"] 

}), 

("Kid-Specific", "YEYARGUP", { 

"question": "How frequently you have arguments with your parents/guardian in a month?", 

"description": "Chose an Average number of times.", 

"answer_type": "radio", 

"options": [None, "0 time", "1 - 2 times", "3 - 5 times", "6 - 9 times", "10 and more times"] 

}), 

("Kid-Specific", "YEPRTDNG", { 

"question": "Does your parents talk about bad effects of drugs?", 

"description": "Select Yes or No.", 

"answer_type": "radio", 

"options": [None, "Yes", "No"] 

}), 

] 

# Function to create the table and populate it
def createQuestion():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name='questions';
    """)
    table_exists = cursor.fetchone()

    if not table_exists:
        # Create the questions table
        cursor.execute("""
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            code TEXT NOT NULL,
            details JSON NOT NULL
        )
        """)
        conn.commit()

        # Insert questions into the database
        for q_type, code, details in questions:
            cursor.execute('INSERT INTO questions (type, code, details) VALUES (?, ?, ?)', 
                           (q_type, code, json.dumps(details)))

        conn.commit()
        print("Questions successfully inserted into the database.")
    else:
        print("Table already exists. No action needed.")

    conn.close()

