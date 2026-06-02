from database_supabase import get_patients
from notifications import send_whatsapp
from datetime import date

patients = get_patients()


today = str(date.today())

for patient in patients:

    name = patient[1]
    phone = patient[3]
    medications = patient[6]
    followup_date = str(patient[7])

    # Recovery Check-In Message

    checkin_msg = f"""
Hello {name},

🩺 Recovery Check-In

How are you feeling today?

Please submit your latest recovery status through the Patient Portal.
https://patient-discharge-agent-wgx8uimu8ufcghxagsaiie.streamlit.app/

After opening the app, select "🧑 Patient Portal" from the sidebar and submit your report.

Please report:

• Current symptoms
• Fever status
• Medication adherence
• Any pain or breathing difficulties

This helps our healthcare team monitor your recovery and provide timely support.

Stay healthy.
"""

    send_whatsapp(
        phone,
        checkin_msg
    )

    # Medication Reminder

    medication_msg = f"""
Hello {name},

💊 Daily Medication Reminder

Please remember to take:

{medications}

Continue following your prescribed treatment plan.

Stay healthy.
"""

    send_whatsapp(
        phone,
        medication_msg
    )

    # Appointment Reminder Only On Follow-Up Date

    if followup_date == today:

        appointment_msg = f"""
Hello {name},

📅 Follow-Up Appointment Reminder

Your follow-up appointment is scheduled for today.

Please submit your recovery report through the Patient Portal before your appointment.
https://patient-discharge-agent-wgx8uimu8ufcghxagsaiie.streamlit.app/

After opening the app, select "🧑 Patient Portal" from the sidebar and submit your report.

Thank you.
"""

        send_whatsapp(
            phone,
            appointment_msg
        )

print("Healthcare Follow-Up Agent execution completed")