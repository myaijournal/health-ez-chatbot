import sys
import os

# Ensure Python can find the "app" package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.utils.db import get_db_connection

def initialize_reschedule_requests_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create reschedule_requests table (if not exists)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reschedule_requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            current_date TEXT,
            requested_date TEXT,
            status TEXT DEFAULT 'Pending',
            note TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Reschedule Requests Database initialized successfully!")

if __name__ == "__main__":
    initialize_reschedule_requests_db()
