import os
from urllib import response
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
    recovery_status,
    recovery_score,
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

    Return in exactly this format:

    ## Risk Level
    <risk>

    ## Reason
    <short reason>

    ## Recommended Action
    <short action>

    Recovery Status: {recovery_status}
    Recovery Score: {recovery_score}/10

    Keep the entire response under 80 words.
    """

    response = model.generate_content(prompt)
    return response.text

