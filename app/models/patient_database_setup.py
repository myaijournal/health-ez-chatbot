import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from config.config import DATABASE_PATH

def initialize_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            diagnosis TEXT,
            current_medication TEXT,
            previous_medication TEXT,
            next_appointment_date TEXT,
            provider TEXT,
            doctor TEXT,
            admission_date TEXT
        )
    ''')

    # Sample data (only insert if table is empty)
    cursor.execute("SELECT COUNT(*) FROM patients")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ("Alice Johnson", 45, "Female", "Diabetes", "Metformin", "Insulin", "2024-03-15", "City Hospital", "Dr. Adams", "2024-02-10"),
            ("Bob Smith", 60, "Male", "Hypertension", "Amlodipine", "Losartan", "2024-03-20", "Greenwood Clinic", "Dr. Patel", "2024-01-15"),
            ("Charlie Brown", 30, "Male", "Flu", "Tamiflu", "None", "2024-02-28", "Downtown Medical", "Dr. Lee", "2024-02-20")
        ]

        cursor.executemany('''
            INSERT INTO patients (name, age, gender, diagnosis, current_medication, previous_medication, 
                                next_appointment_date, provider, doctor, admission_date) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_data)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Run this only when executing the script directly
if __name__ == "__main__":
    initialize_db()
