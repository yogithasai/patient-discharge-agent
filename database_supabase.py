from supabase_client import supabase

def init_db():
    pass


def add_patient(
    name,
    age,
    phone,
    condition,
    discharge_date,
    medications,
    followup_date,
    doctor_id
):

    supabase.table(
        "patients"
    ).insert(
        {
            "name": name,
            "age": age,
            "phone": phone,
            "condition": condition,
            "discharge_date": str(discharge_date),
            "medications": medications,
            "followup_date": str(followup_date),
            "doctor_id": doctor_id
        }
    ).execute()

def get_patients():

    response = supabase.table(
        "patients"
    ).select("*").execute()

    patients = []

    for row in response.data:

        patients.append(
            (
                row["id"],
                row["name"],
                row["age"],
                row["phone"],
                row["condition"],
                row["discharge_date"],
                row["medications"],
                row["followup_date"]
            )
        )

    return patients


def get_patient_names():

    response = supabase.table(
        "patients"
    ).select("name").execute()

    return [
        row["name"]
        for row in response.data
    ]


def get_patient_by_name(name):

    response = supabase.table(
        "patients"
    ).select("*").eq(
        "name",
        name
    ).execute()

    if not response.data:
        return None

    row = response.data[0]

    return (
        row["id"],
        row["name"],
        row["age"],
        row["phone"],
        row["condition"],
        row["discharge_date"],
        row["medications"],
        row["followup_date"]
    )

def add_doctor(
    name,
    specialization,
    email,
    password,
    phone
):

    supabase.table(
        "doctors"
    ).insert(
        {
            "name": name,
            "specialization": specialization,
            "email": email,
            "password": password,
            "phone": phone
        }
    ).execute()

def get_doctors():

    response = supabase.table(
        "doctors"
    ).select("*").execute()

    return response.data

def doctor_login(email, password):

    response = supabase.table(
        "doctors"
    ).select("*").eq(
        "email",
        email
    ).eq(
        "password",
        password
    ).execute()

    if response.data:
        return response.data[0]

    return None

def get_patients_by_doctor(doctor_id):

    response = supabase.table(
        "patients"
    ).select("*").eq(
        "doctor_id",
        doctor_id
    ).execute()

    return response.data

def add_medication_log(
    patient_id,
    medication_name,
    taken,
    taken_time,
    meal_status,
    side_effects
):

    supabase.table(
        "medication_logs"
    ).insert(
        {
            "patient_id": patient_id,
            "medication_name": medication_name,
            "taken": taken,
            "taken_time": taken_time,
            "meal_status": meal_status,
            "side_effects": side_effects
        }
    ).execute()

def get_medication_logs(patient_id):

    response = supabase.table(
        "medication_logs"
    ).select("*").eq(
        "patient_id",
        patient_id
    ).execute()

    return response.data