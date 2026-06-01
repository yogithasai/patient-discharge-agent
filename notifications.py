from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
print("TWILIO SID:", os.getenv("TWILIO_ACCOUNT_SID"))
client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def send_whatsapp(phone, message):

    print("FROM =", os.getenv("TWILIO_WHATSAPP_NUMBER"))
    print("TO =", f"whatsapp:{phone}")

    message = message[:1500]

    twilio_message = client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
        to=f"whatsapp:{phone}"
    )

    return twilio_message.sid

import os

def send_doctor_alert(message):

    return send_whatsapp(
        os.getenv("DOCTOR_WHATSAPP").replace(
            "whatsapp:",
            ""
        ),
        message
    )

def send_staff_alert(
    patient_name,
    symptoms,
    risk_level
):

    alert_message = f"""
    🚨 HIGH RISK PATIENT ALERT

    Patient: {patient_name}

    Risk Level: {risk_level}

    Symptoms:
    {symptoms}

    Immediate review recommended.
    """

    message = client.messages.create(
        body=alert_message[:1500],
        from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
        to=f"whatsapp:{os.getenv('DOCTOR_WHATSAPP')}"
    )

    return message.sid

def send_doctor_alert(message):

    return send_whatsapp(
        os.getenv("DOCTOR_WHATSAPP").replace(
            "whatsapp:", ""
        ),
        message
    )