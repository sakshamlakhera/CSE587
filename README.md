# CSE587
CSE587: Data Intensive Computing
This repository is for CSE587 Data Intensive Project taught by Chen Xu at University at Buffalo.
Repo name might change in future depending on the need. 
If you are seeing this repo and unable to do changes or comment (as it's private) reach out to sakshaml@buffalo.edu

##### NOTE: Do NOT directly commit to develop Branch
##### For changes create a branch with name features/<task_id>_<task_info>, bugs/<task_id>_<task_info>. 
##### Task_ID Will be based on work assignment and task info is the brief info regarding what is the feature or bug. I'm unable to enforce this rule because it's only available to paid user

#### required python packages are in requirements.txt 
#### pip install -r requirement.txt
#### Please execute datafetch notebook before executing other notebooks

#### Team Members
##### Sharan Raj Sivakumar 50604183
##### Apurva Umredkar 50592382
##### Saksham Lakhera 50611360
##### Rama Rao Vydadi 50604256

#### Problem Statement :
This analysis aims to uncover potential causes of mental health disorders by examining the behavioral patterns and histories of affected patients, ### leading to insights for better interventions.

# Data Cleaning Steps
## 1. Handling Sparse Columns
- **Goal**: Identify columns with sparse data and remove or address them.
- **Method**: Columns with more than 10% missing values were considered sparse. 

## 2. Removing Columns with Large Missing Values
- **Goal**: Improve data quality by eliminating columns with excessive missing data.
- **Method**: Any column with a significant portion (over 10%) of missing values was identified from the dataset.

## 3. Filtering for Necessary Columns
- **Goal**: Retain only the relevant columns for analysis.
- **Method**: Non-essential columns were filtered out, leaving only those pertinent to the analysis and model-building steps.

## 4. Type Correction
- **Goal**: Ensure that each column's data type is appropriate for its contents.
- **Method**: The data types of each column were reviewed and corrected where necessary. For example, converting strings representing dates into datetime objects, or strings containing numeric data into integers/floats.

## 5. Duplicate Record Removal
- **Goal**: Eliminate redundant entries that could distort analysis.
- **Method**: Identify and remove duplicate rows to ensure each record is unique.


## 6. Handling Missing Data
- **Goal**: Handle/impute missing Data
- **Method**: Imputed Missing data.

## 6. Data Range validation and cleaning.
- **Goal**: Handle Data Range validation.
- **Method**: using assertions(if statements)

## 7. Substituting Values with Desired Entries
- **Goal**: Substituting Values with Desired Entries
- **Method**: Used .replace functions


### Note: We have performed these cleanings based on EDA and specific requirements for each hypothesis. These cleaning steps are done across different notebooks.  






