from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

print("SID =", repr(os.getenv("TWILIO_ACCOUNT_SID")))
print("TOKEN =", repr(os.getenv("TWILIO_AUTH_TOKEN")))
print("FROM =", repr(os.getenv("TWILIO_WHATSAPP_NUMBER")))

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

message = client.messages.create(
    body="Test",
    from_="whatsapp:+14155238886",
    to="whatsapp:+917036299368"
)

print(message.sid)