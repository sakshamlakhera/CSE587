# utils/db_init.py
from pathlib import Path
from utils.database.connection import DBConnection

class DatabaseInitializer:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.models_dir = Path("models")
    
    def initialize(self):
        """Initialize database and required directories"""
        self._create_directories()
        self._create_tables()
    
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        self.models_dir.mkdir(exist_ok=True)
    
    def _create_tables(self):
        """Create all required database tables"""
        with DBConnection(self.db_path) as conn:
            cursor = conn.cursor()
            
            # User Responses Table
            cursor.execute(self._get_user_responses_table_query())
            
            # Model Predictions Table
            cursor.execute(self._get_predictions_table_query())
            
            # Models Metadata Table
            cursor.execute(self._get_models_table_query())
            
            conn.commit()
    
    @staticmethod
    def _get_user_responses_table_query():
        return '''
            CREATE TABLE IF NOT EXISTS user_responses (
                response_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT NOT NULL,
                
                -- General Information
                Age INTEGER,
                plays_game TEXT,
                Drug_Use TEXT,
                Employment TEXT,
                Education TEXT,
                Income TEXT,
                IRSEX TEXT,
                "HOW OFTEN FELT SAD NOTHING COULD CHEER YOU UP" TEXT,
                sad_depressed TEXT,
                
                -- Gaming Related
                Game TEXT,
                Hours INTEGER,
                Residence TEXT,
                
                -- Substance Use
                MJAGE INTEGER,
                BLNTAGE INTEGER,
                COCAGE INTEGER,
                CRKAGE INTEGER,
                HERAGE INTEGER,
                HALLUCAGE INTEGER,
                METHAMAGE INTEGER,
                
                -- Kid Related
                YEPCHKHW TEXT,
                YEPHLPHW TEXT,
                YO_MDEA2 TEXT,
                YEPCHORE TEXT,
                YEPLMTTV TEXT,
                YEPLMTSN TEXT,
                YO_MDEA1 TEXT,
                YEPGDJOB TEXT,
                YEPPROUD TEXT,
                YEYARGUP TEXT,
                YEPRTDNG TEXT,
                NEWRACE2 TEXT
            )
        '''

    
    
    @staticmethod
    def _get_predictions_table_query():
        return '''
            CREATE TABLE IF NOT EXISTS model_predictions (
                prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                response_id INTEGER,
                model_name TEXT NOT NULL,
                prediction_value REAL,
                prediction_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (response_id) REFERENCES user_responses(response_id)
            )
        '''
    
    @staticmethod
    def _get_models_table_query():
        return '''
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
        '''