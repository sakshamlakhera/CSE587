import sqlite3
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path


class ModelManager:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.loaded_models = {}
        self._create_registry_table()
        self.load_models()

    def _create_registry_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS model_registry (
                    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_name TEXT NOT NULL,
                    model_version TEXT NOT NULL,
                    is_latest BOOLEAN DEFAULT FALSE,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    model_file BLOB NOT NULL,
                    UNIQUE(model_name, model_version)
                )
            ''')
            conn.commit()

    def save_model(self, model_name, model_object, version="1.0", description=""):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Set all existing versions of this model to not latest
            cursor.execute(
                "UPDATE model_registry SET is_latest = FALSE WHERE model_name = ?",
                (model_name,)
            )
            
            model_blob = pickle.dumps(model_object)
            cursor.execute('''
                INSERT OR REPLACE INTO model_registry 
                (model_name, model_version, is_latest, description, model_file)
                VALUES (?, ?, TRUE, ?, ?)
            ''', (model_name, version, description, model_blob))
            conn.commit()

    def load_model(self, model_name, version=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if version:
                cursor.execute('''
                    SELECT model_file FROM model_registry 
                    WHERE model_name = ? AND model_version = ?
                ''', (model_name, version))
            else:
                cursor.execute('''
                    SELECT model_file FROM model_registry 
                    WHERE model_name = ? AND is_latest = TRUE
                ''', (model_name,))
            
            result = cursor.fetchone()
            if result:
                return pickle.loads(result[0])
                # return result[0]
                
            raise ValueError(f"Model {model_name} not found")

    def load_models(self):
        """Load all latest models"""
        model_names = ['gmh_model', 'youth_drug_abuse_model', 
                      'child_behavioral_model', 'general_model']
        for model_name in model_names:
            try:
                self.loaded_models[model_name] = self.load_model(model_name)
            except ValueError:
                print(f"Warning: {model_name} not found in registry")

    def process_gmh_model_responses(self, responses):
        features = {
            "Age": responses['Age'][0],
            "Game": responses['Game'][0],
            "Residence": responses['Residence'][0],
            "Hours": responses['Hours'][0]
            
            
        }
        return pd.DataFrame([features])


    def process_youth_drug_abuse_responses(self, responses):
        base_columns = ['MJAGE', 'BLNTAGE', 'COCAGE', 'CRKAGE', 
                        'HERAGE', 'HALLUCAGE', 'METHAMAGE', 'Drug_Use', 'YO_MDEA1', 'IRSEX']
        # features = {key: responses.get(key, 0) for key in base_columns}
        # df = pd.DataFrame([features])
        df = responses[base_columns]
        print(df)
        print(df.info())
        drug_pairs = {
            'MJEVER': 'MJAGE',
            'BLNTEVER': 'BLNTAGE',
            'COCEVER': 'COCAGE',
            'CRKEVER': 'CRKAGE',
            'HEREVER': 'HERAGE',
            'HALLUCEVR': 'HALLUCAGE',
            'METHAMEVR': 'METHAMAGE'
        }
        
        for ever_col, age_col in drug_pairs.items():
            df[ever_col] = df[age_col].apply(lambda x: 1 if int(x) > 0 else 0)
        
        df['total_drugs_used'] = df[list(drug_pairs.keys())].sum(axis=1)
        df['age_first_drug_use'] = df[list(drug_pairs.values())].replace(0, np.inf).min(axis=1)
        df['age_first_drug_use'] = df['age_first_drug_use'].replace(np.inf, 0)
        
        column_order = ['MJAGE', 'BLNTAGE', 'COCAGE', 'CRKAGE', 'HERAGE', 'HALLUCAGE', 'METHAMAGE', 'Drug_Use', 'MJEVER', 'BLNTEVER', 'COCEVER', 'CRKEVER', 'HEREVER', 'HALLUCEVR', 'METHAMEVR', 'YO_MDEA1', 'IRSEX', 'total_drugs_used', 'age_first_drug_use']
        return df[column_order]

    def process_child_behavioral_responses(self, responses):
        base_columns =[
            'YEPCHKHW', 'YEPHLPHW', 'YEPCHORE', 'YEPLMTTV', 
            'YEPLMTSN', 'YEPGDJOB', 'YEPPROUD', 'YEYARGUP', 
            'NEWRACE2', 'YO_MDEA2', 'YO_MDEA1'
        ]
        for col in base_columns:
                if col in responses.columns:
                    responses[col] = responses[col].map({'Yes': 1, 'No': 2}).fillna(responses[col])    
        return responses[base_columns]

    def process_general_model_responses(self, responses):
        df = responses.copy()
        # Define mappings for categorical variables
        df['High School education'] = 0
        df['education_primary education'] = 0
        # Fill the new columns based on the "Education" column
        
        df.loc[df['Education'] == 0, 'education_primary education'] = 1
        df.loc[df['Education'] == 1, 'education_High School education'] = 1
        # Display the updated DataFrame
        df['Employment_Employed part time']=0
        df['Employment_Other (incl. not in labor force)']=0
        df['Employment_Unemployed']=0
        
        df.loc[df['Employment'] == 0, 'Employment_Employed part time'] = 1
        df.loc[df['Employment'] == 1, 'Employment_Unemployed'] = 1
        df.loc[df['Employment'] == 2, 'Employment_Other (incl. not in labor force)'] = 1
        
        df['income_$50,000 - $74,999']=0
        df['income_$75,000 or more']=0
        df['Less than $20,000']=0
        
        df.loc[df['Income'] == 0, 'income_Less than $20,000'] = 1
        df.loc[df['Income'] == 1, 'income_$50,000 - $74,999'] = 1
        df.loc[df['Income'] == 2, 'income_$75,000 or more'] = 1
        
        
        df['COUNTY METRO/NONMETRO STATUS_Small Metro']=0
        df['COUNTY METRO/NONMETRO STATUS_Non Metro']=0
        
        
        df.loc[df['Metro_NonMetro'] == 0, 'COUNTY METRO/NONMETRO STATUS_Small Metro'] = 1
        df.loc[df['Metro_NonMetro'] == 1, 'COUNTY METRO/NONMETRO STATUS_Non Metro'] = 1
        
        required_cols = ['HOW OFTEN FELT SAD NOTHING COULD CHEER YOU UP', 'Employment_Employed part time', 'Employment_Other (incl. not in labor force)', 'Employment_Unemployed', 'education_High School education', 'education_primary education', 'income_$50,000 - $74,999', 'income_$75,000 or more', 'income_Less than $20,000', 'COUNTY METRO/NONMETRO STATUS_Non Metro', 'COUNTY METRO/NONMETRO STATUS_Small Metro']
        return df[required_cols]

    def run_models(self, responses, model_name):
        """Run all applicable models based on responses"""
        predictions = {}
        
        if model_name == "general_model": 
            general_features = self.process_general_model_responses(responses)
            if 'general_model' in self.loaded_models:
                print("Inside general_model")
                predictions['general_model'] = self.loaded_models['general_model'].predict(general_features)[0]
                print(predictions['general_model'] )

        # Gaming mental health model
        elif model_name == "gmh_model":
            gmh_features = self.process_gmh_model_responses(responses)
            print(f"gmh_features{gmh_features}")
            if gmh_features is not None and 'gmh_model' in self.loaded_models:
                print("Inside gmh_model")
                print(gmh_features)
                predictions['gmh_model'] = self.loaded_models['gmh_model'].predict(gmh_features)[0]
                print(predictions)

        # Youth drug abuse model
        elif model_name == "youth_drug_abuse_model":
            drug_features = self.process_youth_drug_abuse_responses(responses)
            if drug_features is not None and 'youth_drug_abuse_model' in self.loaded_models:
                print("Inside youth_drug_abuse_model")
                predictions['youth_drug_abuse_model'] = self.loaded_models['youth_drug_abuse_model'].predict(drug_features)[0]
                print(predictions)

        elif model_name == "child_behavioral_model":
            child_features = self.process_child_behavioral_responses(responses)
            if child_features is not None and 'child_behavioral_model' in self.loaded_models:
                print(child_features)
                predictions['child_behavioral_model'] = self.loaded_models['child_behavioral_model'].predict(child_features)[0]
                print(predictions['child_behavioral_model'])
        
        return predictions[model_name]
    
if __name__ == "__main__":
    pass
    # models = ModelManager("database.db")

    # Saksham
    # model_input = {'Age': [7],
    #     'Drug_Use': ['No'],
    #     'plays_game': ['No'],
    #     'YEPCHKHW': ['Yes'],
    #     'YEPHLPHW': ['Yes'],
    #     'YO_MDEA2': ['No'],
    #     'YEPCHORE': ['Yes'],
    #     'YEPLMTTV': ['Yes'],
    #     'YEPLMTSN': ['Yes'],
    #     'YO_MDEA1': ['No'],
    #     'YEPGDJOB': ['Yes'],
    #     'YEPPROUD': ['Yes'],
    #     'YEYARGUP': ['Yes'],
    #     'YEPRTDNG': ['Yes'],
    #     'NEWRACE2': [1]}
    
    # model_output = models.run_models(pd.DataFrame.from_dict(model_input), "child_behavioral_model")

    # Apurv
    # model_input = {'Game': [0], 'Hours': [40], 'Residence': [44], 'age_first_marijuana': [18], 'age_first_blunt': [18], 'age_first_cocaine': [18], 'age_first_crack': [18], 'age_first_heroin': [18], 'YEPCHKHW': [0], 'YEPHLPHW': [0], 'YO_MDEA2': [0], 'YEPCHORE': [0], 'YEPLMTTV': [0], 'YEPLMTSN': [0], 'YO_MDEA1': [0], 'YEPGDJOB': [0], 'YEPPROUD': [0], 'YEYARGUP': [0], 'YEPRTDNG': [0], 'Age': [22]}
    
    # model_output = models.run_models(pd.DataFrame.from_dict(model_input), "gmh_model")
    
    # Rama

    # model_input = {
    #     'Employment': [1],
    #     'Education': [1],
    #     'Income': [1],
    #     'IRSEX': [0],
    #     'HOW OFTEN FELT SAD NOTHING COULD CHEER YOU UP': [1],
    #     'sad_depressed': [0],
    #     'Metro_NonMetro': [0]
    # }
    # model_output = models.run_models(pd.DataFrame.from_dict(model_input), "general_model")
    # print(model_output)

    # Sharan 
    # model_input = {'MJAGE': [15], 'BLNTAGE': [0], 'COCAGE': [0], 'CRKAGE': [0], 'HERAGE': [0], 'HALLUCAGE': [0], 'METHAMAGE':[0], 'YO_MDEA1': [2], 'IRSEX': [1], 'Drug_Use': [1]}
    # model_output = models.run_models(pd.DataFrame.from_dict(model_input), "youth_drug_abuse_model")
    # print(model_output)

#     models_to_insert = [
#     {
#         'name': 'gmh_model',
#         'version': '1.0',
#         'path': '/Users/sharanraj/git/CSE587/model/gmh_model.pickle',
#         'description': 'Gaming Mental Health Model'
#     },
#     {
#         'name': 'youth_drug_abuse_model',
#         'version': '1.0',
#         'path': '/Users/sharanraj/git/CSE587/model/youth_drug_abuse_model.pickle',
#         'description': 'Youth Drug Abuse Model'
#     },
#     {
#         'name': 'child_behavioral_model',
#         'version': '1.0',
#         'path': '/Users/sharanraj/git/CSE587/model/child_behavioral_model.pickle',
#         'description': 'Child Behavioral Model'
#     },
#     {
#         'name': 'general_model',
#         'version': '1.0',
#         'path': '/Users/sharanraj/git/CSE587/model/general_model.pkl',
#         'description': 'General Prediction Model'
#     }
# ]
    


#     for model_info in models_to_insert:
#         model_name = model_info['name']
#         model_version = model_info['version']
#         model_path = model_info['path']
#         description = model_info.get('description', '')

#         with open(model_path, 'rb') as f:
#             model_object = pickle.load(f)
#             print(type(model_object))
#             # model_blob = pickle.dumps(model_object)  
#             models.save_model(model_name, model_object, model_version, description)
#             print(f"model: {model_name} saved")






