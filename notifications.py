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