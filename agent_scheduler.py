from database import get_patients
from notifications import send_whatsapp
from datetime import date

patients = get_patients()

today = str(date.today())

for patient in patients:

    name = patient[1]
    phone = patient[3]
    medications = patient[6]
    followup_date = str(patient[7])

    # Medication Reminder
    medication_msg = f"""
Hello {name},

💊 Daily Medication Reminder

Please take:

{medications}

Stay healthy.
"""

    send_whatsapp(phone, medication_msg)

    # Appointment Reminder
    if followup_date == today:

        appointment_msg = f"""
Hello {name},

📅 Follow-Up Appointment Reminder

Your follow-up appointment is today.

Please submit your recovery report through the Patient Portal.
"""

        send_whatsapp(phone, appointment_msg)

print("Agent execution completed")