import pickle
import pandas as pd
from datetime import datetime
from pathlib import Path
from utils.database.connection import DBConnection
from utils.database.init import DatabaseInitializer


class DatabaseManager:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        db_initializer = DatabaseInitializer(db_path)
        db_initializer.initialize() # Initialize database on creation

    def save_response(self, df):
        with DBConnection(self.db_path) as conn:
            response_data = df.iloc[0].to_dict()
            response_data['session_id'] = str(hash(datetime.now()))
            
            columns = ', '.join(response_data.keys())
            placeholders = ', '.join(['?' for _ in response_data])
            query = f"INSERT INTO user_responses ({columns}) VALUES ({placeholders})"
            
            cursor = conn.cursor()
            cursor.execute(query, list(response_data.values()))
            conn.commit()
            return cursor.lastrowid

    def get_responses(self, limit=100):
        with DBConnection(self.db_path) as conn:
            query = '''
                SELECT * FROM user_responses 
                ORDER BY timestamp DESC 
                LIMIT ?
            '''
            return pd.read_sql_query(query, conn, params=(limit,))

    def get_response_by_id(self, response_id):
        with DBConnection(self.db_path) as conn:
            query = "SELECT * FROM user_responses WHERE response_id = ?"
            return pd.read_sql_query(query, conn, params=(response_id,))

    def save_model(self, model_name, model_object, description=""):
        model_path = self.models_dir / f"{model_name}.pkl"
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_object, f)
        
        with DBConnection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO models (model_name, model_path, description, version)
                VALUES (?, ?, ?, '1.0')
                ON CONFLICT(model_name) 
                DO UPDATE SET 
                    model_path=excluded.model_path,
                    last_updated=CURRENT_TIMESTAMP,
                    version=CAST((CAST(version AS FLOAT) + 0.1) AS TEXT)
            ''', (model_name, str(model_path), description))
            conn.commit()
            return cursor.lastrowid

    def load_model(self, model_name):
        with DBConnection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT model_path FROM models WHERE model_name = ?", (model_name,))
            result = cursor.fetchone()
            
            if result:
                model_path = result[0]
                with open(model_path, 'rb') as f:
                    return pickle.load(f)
            return None

    def get_available_models(self):
        with DBConnection(self.db_path) as conn:
            query = "SELECT model_name, version, description FROM models"
            return pd.read_sql_query(query, conn)

    def delete_model(self, model_name):
        with DBConnection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT model_path FROM models WHERE model_name = ?", (model_name,))
            result = cursor.fetchone()
            
            if result:
                model_path = Path(result[0])
                if model_path.exists():
                    model_path.unlink()
                
                cursor.execute("DELETE FROM models WHERE model_name = ?", (model_name,))
                conn.commit()
                return True
            return False

    def save_prediction(self, response_id, model_name, prediction_value):
        with DBConnection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO model_predictions 
                (response_id, model_name, prediction_value)
                VALUES (?, ?, ?)
            ''', (response_id, model_name, prediction_value))
            conn.commit()
            return cursor.lastrowid

    def get_predictions(self, response_id):
        with DBConnection(self.db_path) as conn:
            query = '''
                SELECT model_name, prediction_value, prediction_timestamp 
                FROM model_predictions 
                WHERE response_id = ?
                ORDER BY prediction_timestamp DESC
            '''
            return pd.read_sql_query(query, conn, params=(response_id,))

    def get_all_predictions(self, limit=100):
        with DBConnection(self.db_path) as conn:
            query = '''
                SELECT 
                    r.*, 
                    p.model_name, 
                    p.prediction_value,
                    p.prediction_timestamp
                FROM user_responses r
                JOIN model_predictions p ON r.response_id = p.response_id
                ORDER BY p.prediction_timestamp DESC
                LIMIT ?
            '''
            return pd.read_sql_query(query, conn, params=(limit,))