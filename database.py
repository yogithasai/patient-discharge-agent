import sqlite3

DB_NAME = "patients.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        condition TEXT,
        discharge_date TEXT,
        medications TEXT,
        followup_date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        symptoms TEXT,
        medication_taken TEXT,
        fever TEXT,
        pain_level TEXT,
        breathing_issue TEXT,
        risk_level TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_patient(name, age, condition, discharge_date,
                medications, followup_date):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO patients
    (name, age, condition, discharge_date,
     medications, followup_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (name, age, condition,
     discharge_date, medications,
     followup_date))

    conn.commit()
    conn.close()


def get_patients():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()

    conn.close()
    return data