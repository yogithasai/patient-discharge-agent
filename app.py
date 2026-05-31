from gemini_agent import analyze_patient
import streamlit as st

from gemini_agent import (
    analyze_patient,
    generate_followup_message
)

from database import (
    init_db,
    add_patient,
    get_patients,
    add_followup,
    get_followups,
    get_patient_names,
    get_patient_by_name
)

init_db()

st.title("🏥 Patient Post-Discharge AI Agent")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Register Patient",
        "Patient Follow-Up",
        "Patient Outreach",
        "Staff Alerts",
        "View Patients",
        "Dashboard"
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
    phone = st.text_input(
        "Phone Number"
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
            phone,
            condition,
            discharge_date,
            medications,
            followup_date
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
    
    if patient_name:

        patient = get_patient_by_name(
            patient_name
        )

        if patient:

            st.info(
                f"💊 Medication Reminder: {patient[5]}"
            )

            st.info(
                f"📅 Next Follow-Up Appointment: {patient[6]}"
            )

    symptoms = st.text_area(
        "Describe Symptoms"
    )

    recovery_status = st.selectbox(
        "Recovery Progress",
        [
            "Improving",
            "Same",
            "Worsening"
        ]
    )

    recovery_score = st.slider(
        "Recovery Score (1-10)",
        1,
        10,
        5
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

        add_followup(
                patient_name,
                symptoms,
                medication_taken,
                fever,
                pain_level,
                breathing_issue,
                risk
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
                        recovery_status,
                        recovery_score,
                        medication_taken,
                        fever,
                        pain_level,
                        breathing_issue
                    )

        st.subheader("🤖 AI Medical Assessment")

        st.markdown(ai_result)

elif menu == "Dashboard":

    st.header("📊 Healthcare Dashboard")

    records = get_followups()

    total = len(records)

    high = len(
        [r for r in records if r[7] == "High"]
    )

    medium = len(
        [r for r in records if r[7] == "Medium"]
    )

    low = len(
        [r for r in records if r[7] == "Low"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Assessments",
        total
    )

    col2.metric(
        "High Risk",
        high
    )

    col3.metric(
        "Medium Risk",
        medium
    )

    col4.metric(
        "Low Risk",
        low
    )

    st.subheader("Recent Assessments")

    for record in records:

        st.write(
            f"👤 {record[1]}"
        )

        st.write(
            f"⚠ Risk: {record[7]}"
        )

        st.write(
            f"🩺 Symptoms: {record[2]}"
        )

        st.write("---")

elif menu == "Staff Alerts":

    st.header("🚨 Healthcare Staff Alerts")

    records = get_followups()

    high_risk = [
        r for r in records
        if r[7] == "High"
    ]

    if not high_risk:

        st.success(
            "No active high-risk alerts."
        )

    else:

        for record in high_risk:

            st.error(
                f"""
Patient: {record[1]}

Risk Level: {record[7]}

Symptoms: {record[2]}
"""
            )

elif menu == "Patient Outreach":

    st.header("📩 Patient Outreach Agent")

    patient_names = get_patient_names()

    selected_patient = st.selectbox(
        "Select Patient",
        patient_names
    )

    patient = get_patient_by_name(
        selected_patient
    )

    if patient:

        st.info(
            f"📞 Phone: {patient[3]}"
        )

        st.info(
            f"💊 Medication: {patient[6]}"
        )

        st.info(
            f"📅 Follow-Up: {patient[7]}"
        )

        if st.button(
            "Generate Follow-Up Message"
        ):

            prompt = f"""
            Create a healthcare follow-up message.

            Patient Name:
            {patient[1]}

            Medication:
            {patient[6]}

            Follow-Up Date:
            {patient[7]}

            Ask:
            - Recovery status
            - Fever
            - Pain
            - Breathing issues
            """

            message = generate_followup_message(
                    patient[1],
                    patient[6],
                    patient[7]
                )

            st.subheader(
                "Generated Message"
            )

            st.write(message)