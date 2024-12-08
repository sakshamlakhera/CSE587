This repository is made for the semester-wide project for CSE587 Data Intensive Computing taught by Chen Xu at University at Buffalo (Fall'24 term).
If you are seeing this repository and unable to do changes or comment (as it's private) reach out to sakshaml@buffalo.edu

**NOTE FOR DEVS: Do NOT commit to develop directly, work in branches, and raise pull requests for submission during each phase**

INSTRUCTIONS TO BUILD THE APP FROM SOURCE CODE
---
1. Clone the repository.
2. Create a new virtual environment in python (use Python version 3.13.0) and activate it by using the following commands:
   - ```python3 -m venv <virtual_environment_name>``` or ```conda create <virtual_environment_name>``` if using Anaconda.
   - Activate the environment: ```./<virtual_environment_name>/Scripts/activate``` (Windows) or ```source <virtual_environment_name>/bin/activate``` (macOS/Linux) or ```conda activate <virtual_environment_name>``` (Anaconda)
4. Install all dependencies (python packages with matched versions) by running the command ```pip3 install -r requirements.txt``` in the terminal.
5. Execute the Streamlit app by running the command ```streamlit run app.py``` in the terminal. Web app should open in localhost.

NOTE TO GRADER
---
1. The video demonstration for the web-platform has been uploaded in the root folder named **demo.mp4**
2. The project report has been written in an academic paper format and uploaded in the root folder named **report.pdf**

PROBLEM STATEMENT
---
Analysis to uncover potential causes of mental health disorders.

PROJECT HIGHLIGHTS
---
- We have created an interactive web app for users to take assessment to evaluate the aspect of their mental health they might be struggling with.
- The Streamlit app has been deployed on the Streamlit Community Cloud and can be accessed via the link: https://mentalhealthevaluation.streamlit.app/
   - You may use the following dummy credentials for testing purposes (these are stored in the database):
      - user: saksham@gmail.com
      - password: 1234
- We have added version control to ensure the web app fetches the latest models.

CODE/REPOSITORY STRUCTURE
---
- models - trained machine learning models in .pickle format deployed in the backend of the Streamlit app.
- utils - source code for database setup and user management.
- views - source code for the different pages of the front-end.
- code - backend files
   - core - source code for ML models and database management (version control)
   - utils/database - source code to initialize and connect to the database.
- app.py - main driver program for the web app.
- data.db - holds user specific data & questionnaire data
- database.db - holds backend data (machine learning models)
- requirements.txt - contains all the python packages with versions used in this project. PLEASE INSTALL THESE BEFORE EXECUTING APP LOCALLY.
       
- Notebooks folder:
   - datafetch.ipynb - This file will download the required datasets from the URLs and store them locally. **PLEASE EXECUTE THIS BEFORE RUNNING OTHER INDIVIDUAL NOTEBOOKS.**
   - EDA.ipynb - In this notebook we have gathered information about data-types, missing values, etc in the downloaded datasets. The data cleaning steps performed are noted in the markdowns. (Phase 1)
   - Each team member worked on an individual notebook for phase 1 & phase 2:
      1. Sharan Raj Sivakumar (UB ID#: 50604183)
         - Hypothesis & EDA (Phase 1):(Phase 1 in notebook cells 1-26)
            - Early drug use, particularly during adolescence, is a risk factor for the development of mental health issues.
            - Individuals who are married or widowed are less likely to experience suicidal thoughts compared to individuals who are single.
         - ML Models (Phase 2):(Phase 2 in notebook cells 26-95)
            - Binary classification with Logistic Regression to check if someone has depression.
            - Binary classification using XGBoost to check if someone has depression(Iteration 1 & 2).
            - K-Means clustering to group individuals using various demographic and identitfying clusters with high sucidal thoughts.
  
      2. Apurva Umredkar (UB ID#: 50592382)
         - Hypothesis & EDA (Phase 1 in notebook cells 1-11):
            - Online gamers in countries with higher quality of life have lower levels of anxiety.
            - Younger online gamers have higher anxiety levels and are less satisfied with life.
         - ML Models (Phase 2 in notebook cells 12-29):
            - Clustering + Classification algorithms for identifying mental distress type in online gamers.
            - Regression algorithms for calculating anxiety, satisfaction with life and social phobia levels
       
      3. Saksham Lakhera (UB ID#: 50611360) (I have done my analysis in these files "Saksham_Lakhera_50611360_P2_H1", "Saksham_Lakhera_50611360_P2_H2")
         - Hypotheses & EDA (Phase 1):
            - Is smoking cigarettes a cause of mental health disorders?
            - Does being religious lower te rate of suicidal thoughts?
            - Is insurance a factor for mental health disorders?
            - Parenting behaviors and there affects on a child's mental health.
         - ML Models (Phase 2):
            - Classifier for identifying depression in children
    
      4. Rama Rao Vydadi (UB ID#: 50604256)
         - Hypotheses & EDA (Phase 1 in notebook cells 1-72):
            - What role does marijuana and hallucinogens use play in the aggravation of mental health disorders?
            - How does socio-economic status (income, education, employment status) influence the likelihood of experiencing mental health disorders?
         - ML Models (Phase 2 in notebook cells 73-113):
            - Classifier to detect poor mental health based on hallucinogen and marijuana use.
            - Classifier to detect poor mental health based on socio-economic status.   

      All notebooks have a PDF version in this repository.

**LAST UPDATE:** Dec 7, 2024 (for phase 3 submission)




