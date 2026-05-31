from gemini_agent import analyze_patient
import streamlit as st

from database import (
    init_db,
    add_patient,
    get_patients
)

init_db()

st.title("🏥 Patient Post-Discharge AI Agent")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Register Patient",
        "Patient Follow-Up",
        "View Patients"
    ]
)

if menu == "Register Patient":

    st.header("Patient Registration")

    name = st.text_input("Patient Name")
    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120
    )

    condition = st.text_input(
        "Medical Condition"
    )

    discharge_date = st.date_input(
        "Discharge Date"
    )

    medications = st.text_area(
        "Medications"
    )

    followup_date = st.date_input(
        "Follow-up Date"
    )

    if st.button("Save Patient"):

        add_patient(
            name,
            age,
            condition,
            str(discharge_date),
            medications,
            str(followup_date)
        )

        st.success(
            "Patient Registered Successfully!"
        )

elif menu == "View Patients":

    st.header("Patient Records")

    patients = get_patients()

    for patient in patients:

        st.write(
            f"ID: {patient[0]}"
        )

        st.write(
            f"Name: {patient[1]}"
        )

        st.write(
            f"Condition: {patient[3]}"
        )

        st.write("---")

elif menu == "Patient Follow-Up":

    st.header("Patient Follow-Up Assessment")

    patient_name = st.text_input(
        "Patient Name"
    )

    symptoms = st.text_area(
        "Describe Symptoms"
    )

    medication_taken = st.selectbox(
        "Medication Taken?",
        ["Yes", "No"]
    )

    fever = st.selectbox(
        "Fever?",
        ["No", "Yes"]
    )

    pain_level = st.selectbox(
        "Pain Level",
        ["None", "Mild", "Moderate", "Severe"]
    )

    breathing_issue = st.selectbox(
        "Breathing Difficulty?",
        ["No", "Yes"]
    )

    if st.button("Assess Risk"):

        from risk_assessment import assess_risk

        risk = assess_risk(
            fever,
            pain_level,
            breathing_issue,
            medication_taken
        )

        st.success(
            f"Risk Level: {risk}"
        )

        if risk == "High":
            st.error(
                "⚠ Immediate Doctor Attention Required"
            )

        with st.spinner("AI analyzing patient condition..."):

            ai_result = analyze_patient(
                symptoms,
                medication_taken,
                fever,
                pain_level,
                breathing_issue
            )

        st.subheader("🤖 AI Medical Assessment")

        st.markdown(ai_result)