from gemini_agent import analyze_patient

result = analyze_patient(
    "High fever and severe pain",
    "No",
    "Yes",
    "Severe",
    "Yes"
)

print(result)