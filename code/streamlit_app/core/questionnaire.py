# questionnaire.py
import pandas as pd
from core.config import QUESTION_MAPPINGS
import streamlit as st

class QuestionTree:
    def __init__(self):
        self.responses = {}
        
    def generate_questions(self):
        # General questions for all
        self.responses['Age'] = st.number_input(
            QUESTION_MAPPINGS['general']['Age'], 
            min_value=1, max_value=120, step=1
        )
        self.responses['Drug_Use'] = st.radio(
            QUESTION_MAPPINGS['general']['Drug_Use'], 
            ['Yes', 'No']
        )

        if self.responses['Age'] < 18:
            self._ask_kid_flow()
        elif 18 <= self.responses['Age'] <= 21:
            self._ask_young_adult_flow()
        else:
            self._ask_adult_flow()

        return self._create_dataframe()

    def _ask_kid_flow(self):
        self.responses['plays_game'] = st.radio(
            QUESTION_MAPPINGS['general']['plays_game'], 
            ['Yes', 'No']
        )
        if self.responses['plays_game'] == 'Yes':
            self._ask_gaming_questions()
        if self.responses['Drug_Use'] == 'Yes':
            self._ask_substance_questions()
        self._ask_kid_questions()

    def _ask_young_adult_flow(self):
        self.responses['plays_game'] = st.radio(
            QUESTION_MAPPINGS['general']['plays_game'], 
            ['Yes', 'No']
        )
        self._ask_general_questions()
        if self.responses['plays_game'] == 'Yes':
            self._ask_gaming_questions()
        if self.responses['Drug_Use'] == 'Yes':
            self._ask_substance_questions()

    def _ask_adult_flow(self):
        self._ask_general_questions()
        if self.responses['Drug_Use'] == 'Yes':
            self._ask_substance_questions()

    def _ask_general_questions(self):
        for key, question in QUESTION_MAPPINGS['general'].items():
            if key not in ['Age', 'plays_game', 'Drug_Use']:
                self.responses[key] = st.text_input(question)

    def _ask_gaming_questions(self):
        for key, question in QUESTION_MAPPINGS['gaming'].items():
            if 'Hours' in key:
                self.responses[key] = st.number_input(question, min_value=0, step=1)
            else:
                self.responses[key] = st.text_input(question)

    def _ask_substance_questions(self):
        for key, question in QUESTION_MAPPINGS['substance'].items():
            self.responses[key] = st.number_input(question, min_value=0, step=1)

    def _ask_kid_questions(self):
        for key, question in QUESTION_MAPPINGS['kid'].items():
            self.responses[key] = st.radio(question, ['Yes', 'No'])
        self.responses["NEWRACE2"] = st.number_input(
            QUESTION_MAPPINGS['kid']['NEWRACE2'], 
            min_value=1, max_value=5, step=1
        )

    def _create_dataframe(self):
        df = pd.DataFrame([self.responses])
        return df