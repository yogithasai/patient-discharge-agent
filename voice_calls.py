from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def call_patient(phone_number):

    call = client.calls.create(
        twiml="""
        <Response>
            <Say>
                Alert from CityCare Hospital.
                Your recent follow up assessment indicates that immediate medical attention may be required.
                Please contact your healthcare provider as soon as possible.
            </Say>
        </Response>
        """,
        to=phone_number,
        from_=os.getenv("TWILIO_PHONE_NUMBER")
    )

    return call.sid