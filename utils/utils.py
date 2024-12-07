import pandas as pd
# Default JSON

def tarsformForModel(input_json):
    default_json = {
        'Age': 0,
        'plays_game': 0,
        'Drug_Use': 0,
        'Employment': 0,
        'Education': 0,
        'Income': 0,
        'IRSEX': 0,
        'HOW OFTEN FELT SAD NOTHING COULD CHEER YOU UP': 0,
        'sad_depressed': 0,
        'Game': 0,
        'Hours': 0,
        'Residence': 0,
        'MJAGE': 0,
        'BLNTAGE': 0,
        'COCAGE': 0,
        'CRKAGE': 0,
        'HERAGE': 0,
        'HALLUCAGE': 0,
        'METHAMAGE': 0,
        'YEPCHKHW': 0,
        'YEPHLPHW': 0,
        'YO_MDEA2': 0,
        'YEPCHORE': 0,
        'YEPLMTTV': 0,
        'YEPLMTSN': 0,
        'YO_MDEA1': 0,
        'YEPGDJOB': 0,
        'YEPPROUD': 0,
        'YEYARGUP': 0,
        'YEPRTDNG': 0,
        'Metro_NonMetro':0,
        'NEWRACE2': 0
    }

    # Code to update default JSON
    def update_json(default_json, input_json):
        # Remove leading/trailing spaces from keys in input JSON
        normalized_input = {key.strip(): value for key, value in input_json.items()}
        
        # Update default JSON with normalized input values
        for key, value in normalized_input.items():
            if key in default_json:
                default_json[key] = value
        
        return default_json

    # Update the default JSON
    updated_json = update_json(default_json, input_json)
    df = pd.DataFrame([updated_json])
    return df

