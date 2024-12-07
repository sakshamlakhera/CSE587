from code.streamlit_app.core.modelmanager import ModelManager
import pickle

def createDB():
    import os

    # Print the current working directory
    print("Current Working Directory:", os.getcwd())
    models_to_insert = [
        {
            'name': 'gmh_model',
            'version': '1.0',
            'path': './model/gmh_model.pickle',
            'description': 'Gaming Mental Health Model'
        },
        {
            'name': 'youth_drug_abuse_model',
            'version': '1.0',
            'path': './model/youth_drug_abuse_model.pickle',
            'description': 'Youth Drug Abuse Model'
        },
        {
            'name': 'child_behavioral_model',
            'version': '1.0',
            'path': './model/child_behavioral_model.pickle',
            'description': 'Child Behavioral Model'
        },
        {
            'name': 'general_model',
            'version': '1.0',
            'path': './model/general_model.pkl',
            'description': 'General Prediction Model'
        }
    ]


    models = ModelManager("database.db")
    for model_info in models_to_insert:
        model_name = model_info['name']
        model_version = model_info['version']
        model_path = model_info['path']
        description = model_info.get('description', '')
        if not os.path.exists(model_path):
            print(f"File not found: {model_path}")
        elif os.path.getsize(model_path) == 0:
            print(f"File is empty: {model_path}")
        else:
            print(f"File exists and is not empty: {model_path}")
        is_exist = models.model_exists(model_name, model_version)
        if not is_exist:
            with open(model_path, 'rb') as f:
                
                model_object = pickle.load(f)
                print(type(model_object))
                # model_blob = pickle.dumps(model_object)  
                models.save_model(model_name, model_object, model_version, description)
                print(f"model: {model_name} saved")