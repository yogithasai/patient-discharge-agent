import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def analyze_patient(
    symptoms,
    medication_taken,
    fever,
    pain_level,
    breathing_issue
):

    prompt = f"""
    You are a healthcare follow-up assistant.

    Analyze the patient's condition.

    Symptoms: {symptoms}
    Medication Taken: {medication_taken}
    Fever: {fever}
    Pain Level: {pain_level}
    Breathing Difficulty: {breathing_issue}

    Return ONLY:

    Risk Level:
    Reason: (max 2 lines)
    Recommended Action: (max 2 lines)

    Keep the entire response under 100 words.
    """