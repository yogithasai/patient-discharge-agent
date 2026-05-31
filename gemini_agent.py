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
    Analyze this discharged patient's condition.

    Symptoms: {symptoms}
    Medication Taken: {medication_taken}
    Fever: {fever}
    Pain Level: {pain_level}
    Breathing Difficulty: {breathing_issue}

    Return:

    Risk Level:
    Reason:
    Recommended Action:
    """

    response = model.generate_content(prompt)

    return response.text