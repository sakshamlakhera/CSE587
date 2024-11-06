This repository is made for the semester-wide project for CSE587 Data Intensive Computing taught by Chen Xu at University at Buffalo (Fall'24 term).
If you are seeing this repo and unable to do changes or comment (as it's private) reach out to sakshaml@buffalo.edu

**NOTE: Do NOT commit to develop directly, work in branches, and raise pull requests for submission during each phase**

Required python packages are in requirements.txt 
- pip install -r requirement.txt

### Team Problem Statement :
Analysis to uncover potential causes of mental health disorders.

Code structure:
- datafetch.ipynb - This file will download the required datasets from the URLs and store them locally. **PLEASE EXECUTE THIS BEFORE RUNNING OTHER INDIVIDUAL NOTEBOOKS.**
- EDA.ipynb - In this notebook we have gathered information about data-types, missing values, etc in the downloaded datasets. The data cleaning steps performed are noted in the markdowns. (Phase 1)

Each team member has an individual notebook:
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

**LAST UPDATE:** Nov 5, 2024 (for phase 2 submission)




