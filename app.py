from gemini_agent import analyze_patient
import streamlit as st

st.set_page_config(
    page_title="Patient Post-Discharge AI Agent",
    page_icon="🏥",
    layout="wide"
)

from notifications import (
    send_whatsapp,
    send_staff_alert
)

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

st.markdown("""
    <style>

    .main {
        padding-top: 1rem;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        font-weight: bold;
    }

    div[data-testid="metric-container"] {
        border: 1px solid #e6e6e6;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    }

    </style>
    """, unsafe_allow_html=True)

init_db()

st.markdown("""
    # 🏥 Patient Post-Discharge AI Agent
    ### AI-Powered Recovery Monitoring & Healthcare Outreach
    """)

st.sidebar.title("🏥 Healthcare AI")
st.sidebar.caption("Patient Post-Discharge Monitoring System")
st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "Navigation",
    [
         "📊 Dashboard",
        "👤 Register Patient",
        "🩺 Patient Follow-Up",
        "📩 Patient Outreach",
        "📅 Reminder Center",
        "🚨 Staff Alerts",
        "📋 View Patients"
    ]
)

st.sidebar.markdown("---")
patients = get_patients()

count = len(patients)

st.sidebar.warning(
    f"🔔 {count} Patients Pending Follow-Up"
)

with st.sidebar.expander(
    "View Follow-Up Queue"
):

    for p in patients:

        st.write(
            f"👤 {p[1]}"
        )

        st.caption(
            f"📅 {p[7]}"
        )

st.sidebar.info(
    "AI-powered patient recovery monitoring and healthcare outreach."
)

if menu == "👤 Register Patient":
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

elif menu == "📋 View Patients":

    st.header("📋Patient Records")

    patients = get_patients()
    st.metric(
    "👥 Registered Patients",
    len(patients)
)

    for patient in patients:

        with st.container():

            st.markdown(
                f"### 👤 {patient[1]}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.info(
                    f"📞 Phone\n\n{patient[3]}"
                )

                st.info(
                    f"🏥 Condition\n\n{patient[4]}"
                )

            with col2:

                st.info(
                    f"💊 Medication\n\n{patient[6]}"
                )

                st.info(
                    f"📅 Follow-Up\n\n{patient[7]}"
                )

            st.divider()

elif menu == "🩺 Patient Follow-Up":

    st.header("Patient Follow-Up Assessment")

    patient_names = get_patient_names()

    patient_name = st.selectbox(
        "Select Patient",
        patient_names
    )
    

    if patient_name:

        patient = get_patient_by_name(
            patient_name
        )

        if patient:

            st.info(
                f"💊 Medication Reminder: {patient[6]}"
            )

            st.info(
                f"📅 Next Follow-Up Appointment: {patient[7]}"
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
        patient = get_patient_by_name(patient_name)

        if not patient:
            st.error(
                "❌ Patient not found. Please register the patient first."
            )
            st.stop()

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

            from notifications import send_doctor_alert

            alert_message = f"""
        🚨 HIGH RISK PATIENT ALERT

        Patient: {patient_name}

        Symptoms: {symptoms}

        Fever: {fever}
        Pain: {pain_level}
        Breathing Issue: {breathing_issue}

        Immediate review recommended.
        """

            send_doctor_alert(
                alert_message
            )

        if "high" in risk.lower() or "critical" in risk.lower():

            st.error(
                "⚠ Immediate Doctor Attention Required"
            )

            staff_sid = send_staff_alert(
                patient_name,
                symptoms,
                risk
            )

            st.warning(
                "🚨 Staff Alert Sent Successfully"
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

elif menu == "📊 Dashboard":

    st.header("📊 Healthcare Dashboard")

    records = get_followups()
    patients = get_patients()

    total_patients = len(patients)

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
    "👥 Patients",
    total_patients
    )

    col2.metric(
    "🚨 High Risk",
    high
    )   

    col3.metric(
    "⚠ Medium Risk",
    medium
    )

    col4.metric(
    "✅ Low Risk",
    low
    )

    st.markdown("---")

    st.subheader("🏥 System Overview")

    st.info(
        f"""
    Total Registered Patients: {total_patients}

    Total Follow-Up Assessments: {total}

    High Risk Cases: {high}

    WhatsApp Outreach Enabled: ✅

    Healthcare Staff Alerts Enabled: ✅
    """
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

elif menu == "📅 Reminder Center":

    st.header("📅 Reminder Center")

    patients = get_patients()

    st.metric(
        "Patients Eligible For Reminders",
        len(patients)
    )

    st.markdown("---")

    if st.button(
        "💊 Send Medication Reminders"
    ):

        sent = 0

        for patient in patients:

            reminder = f"""
    Hello {patient[1]},

    💊 Medication Reminder

    Please remember to take:

    {patient[6]}

    Reply if you are experiencing:
    • Fever
    • Pain
    • Breathing difficulty

    Stay healthy.
    """

            send_whatsapp(
                patient[3],
                reminder
            )

            sent += 1

        st.success(
            f"✅ Medication reminders sent to {sent} patients."
        )

    if st.button(
        "📅 Send Appointment Reminders"
    ):

        sent = 0

        for patient in patients:

            reminder = f"""
Hello {patient[1]},

📅 Appointment Reminder

Your follow-up appointment is scheduled for:

{patient[7]}

Please contact the hospital if you need to reschedule.

Thank you.
"""

            send_whatsapp(
                patient[3],
                reminder
            )

            sent += 1

        st.success(
            f"✅ Appointment reminders sent to {sent} patients."
        )

elif menu == "🚨 Staff Alerts":

    st.header("🚨 Healthcare Alert Center")

    records = get_followups()

    high_risk = [
        r for r in records
        if r[7] == "High"
    ]

    st.metric(
        "Active High-Risk Alerts",
        len(high_risk)
    )

    st.markdown("---")

    if not high_risk:

        st.success(
            "✅ No active high-risk patients."
        )

    else:

        for record in high_risk:

            with st.container():

                st.error(
                    f"🚨 HIGH RISK PATIENT: {record[1]}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"🩺 Symptoms: {record[2]}"
                    )

                with col2:

                    st.write(
                        f"⚠ Risk Level: {record[7]}"
                    )

                st.warning(
                    "Immediate healthcare staff review recommended."
                )

                st.divider()

elif menu == "📩 Patient Outreach":
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
            Generate a WhatsApp message under 500 characters.

            Patient: {patient[1]}
            Medication: {patient[6]}
            Follow-up Date: {patient[7]}

            Include:
            - Medication reminder
            - Follow-up reminder
            - Ask recovery status
            - Ask about fever, pain, breathing issues

            Keep it friendly and concise.
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

            sid = send_whatsapp(
                patient[3],
                message
            )

            st.success(
                f"✅ WhatsApp Sent Successfully!"
            )

            st.write(
                f"Message SID: {sid}"
            )