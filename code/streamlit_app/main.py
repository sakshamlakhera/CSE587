import streamlit as st

from core.questionnaire import QuestionTree
from core.modelmanager import ModelManager
from core.mcdm import MCDMManager
from core.dbmanager import DatabaseManager

class AppController:
    def __init__(self, db_path="database.db"):
        
        # Initialize session state if not exists
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.current_step = 'questionnaire'
            st.session_state.responses = None
            st.session_state.model_results = None

        self.db = DatabaseManager(db_path)
        self.questionnaire = QuestionTree()
        self.models = ModelManager(db_path)
        self.mcdm = MCDMManager()

    def render_sidebar(self):
        with st.sidebar:
            st.title("Navigation")
            if st.button("Start Over"):
                st.session_state.current_step = 'questionnaire'
                st.session_state.responses = None
                st.session_state.model_results = None
                st.rerun()

    def run(self):
        self.render_sidebar()
        
        st.title("Mental Health Analysis System")

        if st.session_state.current_step == 'questionnaire':
            self.run_questionnaire()
        elif st.session_state.current_step == 'models':
            self.run_models()
        elif st.session_state.current_step == 'analysis':
            self.run_analysis()

    def run_questionnaire(self):
        st.header("Questionnaire")
        
        # Get responses from questionnaire
        df = self.questionnaire.generate_questions()
        print(df)
        
        # Show next step button only if we have responses
        if df is not None and not df.empty:
            st.session_state.responses = df
            if st.button("Save and Continue to Models"):
                # Save responses to database
                self.db.save_response(df)
                st.session_state.current_step = 'models'
                st.rerun()

    def run_models(self):
        st.header("Model Analysis")
        
        if st.session_state.responses is None:
            st.error("No questionnaire responses found. Please complete the questionnaire first.")
            if st.button("Back to Questionnaire"):
                st.session_state.current_step = 'questionnaire'
                st.rerun()
            return

        # Run selected models
        model_results = self.models.run_models(st.session_state.responses)

        print(model_results)
        
        if model_results:
            st.session_state.model_results = model_results
            if st.button("Continue to Analysis"):
                st.session_state.current_step = 'analysis'
                st.rerun()

    def run_analysis(self):
        st.header("Final Analysis")
        
        if st.session_state.model_results is None:
            st.error("No model results found. Please run the models first.")
            if st.button("Back to Models"):
                st.session_state.current_step = 'models'
                st.rerun()
            return

        # Run TOPSIS analysis
        final_results = self.mcdm.run_topsis(st.session_state.model_results)
        
        # Display results
        st.write("Analysis Results:", final_results)
        
        if st.button("Start New Analysis"):
            st.session_state.current_step = 'questionnaire'
            st.session_state.responses = None
            st.session_state.model_results = None
            st.rerun()

def main():
    st.set_page_config(
        page_title="Mental Health Analysis System",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    app = AppController()
    app.run()

if __name__ == "__main__":
    main()