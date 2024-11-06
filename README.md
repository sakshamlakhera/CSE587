This repository is made for the semester-wide project for CSE587 Data Intensive Computing taught by Chen Xu at University at Buffalo (Fall'24 term).
If you are seeing this repo and unable to do changes or comment (as it's private) reach out to sakshaml@buffalo.edu

**NOTE: Do NOT commit to develop directly, work in branches, and raise pull requests for submission during each phase**

#### required python packages are in requirements.txt 
#### pip install -r requirement.txt

### Team Problem Statement :
Analysis to uncover potential causes of mental health disorders.

Code structure:
- datafetch.ipynb - This file will download the required datasets from the URLs and store them locally. **PLEASE EXECUTE THIS BEFORE RUNNING OTHER INDIVIDUAL NOTEBOOKS.**
- EDA.ipynb - In this notebook we have gathered information about data-types, missing values, etc in the downloaded datasets. The data cleaning steps performed are noted in the markdowns. (Phase 1)

Each team member has an individual notebook:
1. Sharan Raj Sivakumar (UB ID#: 50604183)
   - Hypothesis & EDA (Phase 1):
     - Early drug use, particularly during adolescence, is a risk factor for the development of mental health issues.
     - Individuals who are married or widowed are less likely to experience suicidal thoughts compared to individuals who are single.
   - ML Models (Phase 2):
     - Binary classification using XGBoost to check if someone has depression.
      
2. Apurva Umredkar (UB ID#: 50592382)
   - Hypothesis & EDA (Phase 1):
     - Online gamers in countries with higher quality of life have lower levels of anxiety.
     - Younger online gamers have higher anxiety levels and are less satisfied with life.
   - ML Models (Phase 2):
     - Clustering + Classification algorithms for identifying mental distress type in online gamers.
       
4. Saksham Lakhera (UB ID#: 50611360)
   - Hypotheses & EDA (Phase 1):
     - Is smoking cigarettes a cause of mental health disorders?
     - Does being religious lower te rate of suicidal thoughts?
     - Is insurance a factor for mental health disorders?
     - Parenting behaviors and there affects on a child's mental health.
   - ML Models (Phase 2):
     - Classifier for identifying depression in children
     - 
    
5. Rama Rao Vydadi (UB ID#: 50604256)
   - Hypotheses & EDA (Phase 1):
     - How does socio-economic status (income, education, employment status) influence the likelihood of experiencing mental health disorders?
     - What role does marijuana use play in the aggravation of mental health disorders?
     - What roles does hallucinogens play in mental health disorders?
   - ML Models (Phase 2):
     - Classifier to check if a person has bad mental health condition based on hallucinogens & marijuana use.
     - Classifier to check if a person has bad mental health condition based on socio-economic status.   

All notebooks have a PDF version in this repository.

**LAST UPDATE: Nov 5, 2024 (for phase 2 submission)




