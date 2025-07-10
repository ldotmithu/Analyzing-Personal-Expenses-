# database_setup.py
import pandas as pd
import sqlite3
from generate_data import generate_expense_data 

DB_NAME = 'expenses.db'

def setup_database(df: pd.DataFrame):
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

       
        cursor.execute("DROP TABLE IF EXISTS expenses;")

        
        cursor.execute('''
            CREATE TABLE expenses (
                Date TEXT NOT NULL,
                Category TEXT NOT NULL,
                Payment_Mode TEXT NOT NULL,
                Description TEXT,
                Amount_Paid REAL NOT NULL,
                Cashback REAL DEFAULT 0.0
            );
        ''')
        conn.commit()
        print(f"Table 'expenses' created successfully in {DB_NAME}.")

        
        df.to_sql('expenses', conn, if_exists='append', index=False)
        print(f"Successfully loaded {len(df)} records into 'expenses' table.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    expense_df = generate_expense_data(num_months=12, start_year=2024)
    print("Expense data generated. Proceeding to database loading.")
    setup_database(expense_df)
    print("Database setup complete.")
    
    conn = sqlite3.connect(DB_NAME)
    verification_df = pd.read_sql_query("SELECT * FROM expenses LIMIT 5;", conn)
    print("Verifying data in the database (first 5 rows):")
    print(verification_df)
    conn.close()