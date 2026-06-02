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
        phone TEXT,
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
            risk_level TEXT,
            status TEXT
        )
        """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patient_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        symptoms TEXT,
        medication_taken TEXT,
        fever TEXT,
        report_risk TEXT,
        report_status TEXT
    )
    """)

    conn.commit()
    conn.close()
    
def add_patient(name, age, phone,
                condition,
                discharge_date,
                medications,
                followup_date):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patients
        (name, age, phone,
        condition,
        discharge_date,
        medications,
        followup_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            age,
            phone,
            condition,
            discharge_date,
            medications,
            followup_date
        ))
    conn.commit()
    conn.close()


def get_patients():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()

    conn.close()
    return data

def add_followup(
    patient_name,
    symptoms,
    medication_taken,
    fever,
    pain_level,
    breathing_issue,
    risk_level
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if risk_level == "High":
        status = "Escalated"

    elif risk_level == "Medium":
        status = "Pending"

    else:
        status = "Reviewed"

    cursor.execute("""
        INSERT INTO followups
        (
            patient_name,
            symptoms,
            medication_taken,
            fever,
            pain_level,
            breathing_issue,
            risk_level,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            patient_name,
            symptoms,
            medication_taken,
            fever,
            pain_level,
            breathing_issue,
            risk_level,
            status
        ))

    conn.commit()
    conn.close()

def get_followups():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM followups
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data

def get_patient_by_name(name):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE name = ?",
        (name,)
    )

    patient = cursor.fetchone()

    conn.close()

    return patient

def get_patient_names():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM patients"
    )

    names = cursor.fetchall()

    conn.close()

    return [n[0] for n in names]

def add_patient_report(
    patient_name,
    symptoms,
    medication_taken,
    fever,
    report_risk,
    report_status
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO patient_reports
    (
        patient_name,
        symptoms,
        medication_taken,
        fever,
        report_risk,
        report_status
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        patient_name,
        symptoms,
        medication_taken,
        fever,
        report_risk,
        report_status
    ))

    conn.commit()
    conn.close()

def get_patient_reports():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM patient_reports
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data

def delete_patient(name):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE name = ?",
        (name,)
    )

    cursor.execute(
        "DELETE FROM followups WHERE patient_name = ?",
        (name,)
    )

    cursor.execute(
        "DELETE FROM patient_reports WHERE patient_name = ?",
        (name,)
    )

    conn.commit()
    conn.close()

def get_latest_followup(patient_name):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM followups
        WHERE patient_name = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (patient_name,)
    )

    data = cursor.fetchone()

    conn.close()

    return data

def clear_all_data():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients")
    cursor.execute("DELETE FROM followups")
    cursor.execute("DELETE FROM patient_reports")

    conn.commit()
    conn.close()
