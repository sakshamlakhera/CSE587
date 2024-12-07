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
        self.load_models()


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
        print(type(responses['plays_game']))
        print(responses.get('plays_game'))
        if responses['plays_game'][0] == 'Yes':
            features = {
                "Age": responses['Age'][0],
                "Game": responses['Game'][0],
                "Hours": responses['Hours'][0],
                "Residence": responses['Residence'][0]
            }
            return pd.DataFrame([features])
        return None

    def process_youth_drug_abuse_responses(self, responses):
        if responses['Drug_Use'][0] == 'Yes':
            base_columns = ['MJAGE', 'BLNTAGE', 'COCAGE', 'CRKAGE', 
                          'HERAGE', 'HALLUCAGE', 'METHAMAGE', 'YO_MDEA2', 'IRSEX']
            # features = {key: responses.get(key, 0) for key in base_columns}
            # df = pd.DataFrame([features])
            df = responses[base_columns]
            
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
                df[ever_col] = df[age_col].apply(lambda x: 1 if x > 0 else 0)
            
            df['total_drugs_used'] = df[list(drug_pairs.keys())].sum(axis=1)
            df['age_first_drug_use'] = df[list(drug_pairs.values())].replace(0, np.inf).min(axis=1)
            df['age_first_drug_use'] = df['age_first_drug_use'].replace(np.inf, 0)
            
            return df
        return None

    def process_child_behavioral_responses(self, responses):
        if responses['Age'][0] < 18:
            base_columns =[
                'YEPCHKHW', 'YEPHLPHW', 'YEPCHORE', 'YEPLMTTV', 
                'YEPLMTSN', 'YEPGDJOB', 'YEPPROUD', 'YEYARGUP', 
                'NEWRACE2', 'YO_MDEA2', 'YO_MDEA1'
            ]
            for col in base_columns:
                if col in responses.columns:
                    responses[col] = responses[col].map({'Yes': 1, 'No': 2}).fillna(responses[col])
        
            return responses[base_columns]
        return None

    def process_general_model_responses(self, responses):
        # Define mappings for categorical variables
        mappings = {
            'Employment': ["Employed part time", "Other (incl. not in labor force)", "Unemployed"],
            'Education': ["High School education", "Primary education"],
            'Income': ["$50,000 - $74,999", "$75,000 or more", "Less than $20,000"],
            'CountyStatus': ["Non Metro", "Small Metro"]
        }
        
        # Initialize transformed features
        transformed = {}
        
        # One-hot encode categorical variables
        for feature, categories in mappings.items():
            value = responses.get(feature)
            for category in categories:
                col_name = f"{feature}_{category}"
                transformed[col_name] = 1 if value == category else 0
        
        # Add non-categorical features
        transformed["HOW OFTEN FELT SAD NOTHING COULD CHEER YOU UP"] = responses.get(
            "HOW OFTEN FELT SAD NOTHING COULD CHEER YOU UP"
        )
        transformed["IRSEX"] = responses.get("IRSEX")
        
        return pd.DataFrame([transformed])

    def run_models(self, responses):
        """Run all applicable models based on responses"""
        predictions = {}
        
        # General model (always runs)
        responses.to_csv("dummy.csv")
        general_features = self.process_general_model_responses(responses)
        if 'general_model' in self.loaded_models:
            print("Inside general_model")
            predictions['general_model'] = self.loaded_models['general_model'].predict(general_features)[0]
            print(predictions['general_model'] )
        print(2, type(responses))
        # Gaming mental health model
        gmh_features = self.process_gmh_model_responses(responses)
        print(f"gmh_features{gmh_features}")
        if gmh_features is not None and 'gmh_model' in self.loaded_models:
            print("Inside gmh_model")
            predictions['gmh_model'] = self.loaded_models['gmh_model'].predict(gmh_features)[0]
            print(predictions)
        # Youth drug abuse model
        drug_features = self.process_youth_drug_abuse_responses(responses)
        if drug_features is not None and 'youth_drug_abuse_model' in self.loaded_models:
            print("Inside youth_drug_abuse_model")
            predictions['youth_drug_abuse_model'] = self.loaded_models['youth_drug_abuse_model'].predict(drug_features)[0]
            print(predictions)
        # Child behavioral model
        child_features = self.process_child_behavioral_responses(responses)
        if child_features is not None and 'child_behavioral_model' in self.loaded_models:
            print("Inside youth_drug_abuse_model")
            print(child_features)
            predictions['child_behavioral_model'] = self.loaded_models['child_behavioral_model'].predict(child_features)[0]
            print(predictions['child_behavioral_model'])
        
        return predictions
    
if __name__ == "__main__":
    models = ModelManager("database.db")

    models_to_insert = [
    {
        'name': 'gmh_model',
        'version': '1.0',
        'path': '/Users/sharanraj/git/CSE587/model/gmh_model.pickle',
        'description': 'Gaming Mental Health Model'
    },
    {
        'name': 'youth_drug_abuse_model',
        'version': '1.0',
        'path': '/Users/sharanraj/git/CSE587/model/gmh_model.pickle',
        'description': 'Youth Drug Abuse Model'
    },
    {
        'name': 'child_behavioral_model',
        'version': '1.0',
        'path': '/Users/sharanraj/git/CSE587/model/child_behavioral_model.pickle',
        'description': 'Child Behavioral Model'
    },
    {
        'name': 'general_model',
        'version': '1.0',
        'path': '/Users/sharanraj/git/CSE587/model/general_model.pkl',
        'description': 'General Prediction Model'
    }
]
    


    for model_info in models_to_insert:
        model_name = model_info['name']
        model_version = model_info['version']
        model_path = model_info['path']
        description = model_info.get('description', '')

        with open(model_path, 'rb') as f:
            model_object = pickle.load(f)
            print(type(model_object))
            # model_blob = pickle.dumps(model_object)  
            models.save_model(model_name, model_object, model_version, description)
            print(f"model: {model_name} saved")






