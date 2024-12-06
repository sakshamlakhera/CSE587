import sqlite3

def check_database_data():
    DB_PATH = "database.db"
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # Check user_responses table
            cursor.execute("SELECT * FROM user_responses")
            responses_count = cursor.fetchone()
            print(f"User responses count: {responses_count}")
            
            # Check model_predictions table
            cursor.execute("SELECT COUNT(*) FROM model_predictions")
            predictions_count = cursor.fetchone()[0]
            print(f"Model predictions count: {predictions_count}")
            
            # Check models table
            cursor.execute("SELECT COUNT(*) FROM models")
            models_count = cursor.fetchone()[0]
            print(f"Models count: {models_count}")
            
    except sqlite3.OperationalError as e:
        print(f"Database error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

check_database_data()