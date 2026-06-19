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

supabase.table("patients").insert(
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