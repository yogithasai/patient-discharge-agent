from database_sqlite_backup import get_patients
from notifications import send_medication_reminder
from notifications import send_appointment_reminder

def run_daily_tasks():

    patients = get_patients()

    for patient in patients:

        send_medication_reminder(patient)

        send_appointment_reminder(patient)

if __name__ == "__main__":
    run_daily_tasks()