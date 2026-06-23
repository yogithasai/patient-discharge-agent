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

from database_supabase import (
    init_db,
    add_patient,
    get_patients,
    get_patient_names,
    get_patient_by_name,
    add_doctor,
    doctor_login,
    get_doctors,
    get_patients_by_doctor
)

from database import (
    add_followup,
    get_followups,
    add_patient_report,
    get_patient_reports,
    delete_patient,
    get_latest_followup,
    update_followup_status
)

from database import init_db

init_db()

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
    ### Automated Post-Discharge Monitoring, Risk Detection & Patient Recovery Management
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
        "🤖 Follow-Up Agent",
        "💊 Care Reminders",
        "🚨 Alert Center",
        "📋 View Patients",
        "📝 Patient Portal",
        "👨‍⚕️ Doctor Portal"
    ]
)

st.sidebar.markdown("---")
patients = get_patients()

count = len(patients)

st.sidebar.info(
    f"👥 {count} Registered Patients"
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

    with st.form("patient_form", clear_on_submit=True):

        name = st.text_input("Patient Name")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=18
        )

        phone = st.text_input(
            "Phone Number",
        ).strip()

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

        doctors = get_doctors()

        if doctors:

            doctor_names = [doctor["name"] for doctor in doctors]

            selected_doctor = st.selectbox(
                "Assign Doctor",
                doctor_names
            )

        else:

            st.warning("No doctors registered yet.")
            selected_doctor = None
            
        submitted = st.form_submit_button(
            "Save Patient"
        )

    if submitted:

        if not name.strip():

            st.error(
                "Patient name is required"
            )

        elif not phone.isdigit() or len(phone) != 10:

            st.error(
                "Enter a valid 10-digit phone number"
            )

        elif followup_date < discharge_date:

            st.error(
                "Follow-up date cannot be before discharge date"
            )

        else:

            formatted_phone = "+91" + phone

            doctor_id = None

            if selected_doctor:

                doctor_id = next(
                    doctor["id"]
                    for doctor in doctors
                    if doctor["name"] == selected_doctor
                )

            add_patient(
                name,
                age,
                formatted_phone,
                condition,
                discharge_date,
                medications,
                followup_date,
                doctor_id
            )

            st.success(
                f"✅ {name} registered successfully"
            )

            welcome_message = f"""
                    🏥 Welcome to the Patient Recovery Monitoring Program

                    Hello {name},

                    You have been successfully enrolled in our post-discharge follow-up program.

                    You will receive:

                    ✅ Medication reminders
                    ✅ Appointment reminders
                    ✅ Recovery check-ins

                    If you experience fever, pain, or breathing difficulties, please report them immediately.
                    https://patient-discharge-agent-wgx8uimu8ufcghxagsaiie.streamlit.app/
                    
                    After opening the app, select "🧑 Patient Portal" from the sidebar and submit your report.


                    Wishing you a smooth recovery.
                    """

            send_whatsapp(
                        formatted_phone,
                        welcome_message
                    )

            st.info(
                        "📩 Patient onboarding message sent."
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
            latest_followup = get_latest_followup(patient[1])

            if latest_followup:

                st.info(
                    f"⚠ Latest Risk: {latest_followup[7]}"
                )

            if st.button(
                f"🗑 Delete {patient[1]}",
                key=f"delete_{patient[0]}"
            ):

                delete_patient(patient[1])

                st.success(
                    f"✅ {patient[1]} deleted successfully"
                )

                st.rerun()

            st.divider()


elif menu == "📝 Patient Portal":

    st.header("📝 Patient Self-Report Portal")

    patient_names = get_patient_names()

    selected_patient = st.selectbox(
        "Select Patient",
        patient_names
    )

    with st.form(
    "patient_report_form",
    clear_on_submit=True
):

        symptoms = st.text_area(
            "Current Symptoms"
        )

        medication_taken = st.selectbox(
            "Medication Taken?",
            ["Yes", "No"]
        )

        fever = st.selectbox(
            "Do you currently have fever?",
            ["No", "Yes"]
        )

        submitted = st.form_submit_button(
            "Submit Self Report"
        )

    if submitted:

        score = 0

        if fever == "Yes":
            score += 4

        if medication_taken == "No":
            score += 3

        if len(symptoms) > 30:
            score += 3

        if score >= 7:
            risk = "High"
            status = "Escalated"

        elif score >= 4:
            risk = "Medium"
            status = "Pending"

        else:
            risk = "Low"
            status = "Reviewed"

        add_patient_report(
            selected_patient,
            symptoms,
            medication_taken,
            fever,
            risk,
            status
        )

        if risk == "High":

            from notifications import send_doctor_alert

            send_doctor_alert(
                f"""
        🚨 HIGH RISK PATIENT SELF REPORT

        Patient: {selected_patient}

        Symptoms: {symptoms}

        Medication Taken: {medication_taken}

        Fever: {fever}

        Risk: {risk}

        Immediate review required.
        """
            )

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
    
    with st.form("followup_form", clear_on_submit=True):

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

        submitted = st.form_submit_button(
            "Assess Risk"
        )

    if submitted:
        patient = get_patient_by_name(patient_name)

        if not patient:
            st.error(
                "❌ Patient not found. Please register the patient first."
            )
            st.stop()

        from risk_assessment import assess_risk

        if not symptoms.strip():

            st.error(
                "Please describe patient symptoms"
            )

            st.stop()
            
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
            f"✅ Assessment Completed | Risk Level: {risk}"
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

    reports = get_patient_reports()

    total_reports = len(reports)


    total_patients = len(patients)

    total = len(records)

    high = len(
    [
        r for r in records
        if r[7] == "High"
        and r[8] != "Reviewed"
    ]
)

    medium = len(
        [r for r in records if r[7] == "Medium"]
    )

    low = len(
        [r for r in records if r[7] == "Low"]
    )

    escalated = len(
        [
            r for r in records
            if r[8] == "Escalated"
        ]
    )

    pending = len(
        [r for r in records if r[8] == "Pending"]
    )

    reviewed = len(
        [r for r in records if r[8] == "Reviewed"]
    )

    pending_followups = len(patients)

    col1, col2, col3, col4, col5 = st.columns(5)

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

    col5.metric("📝 Reports", total_reports)

    st.markdown("---")
    st.subheader("📌 Case Status Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🚨 Escalated",
        escalated
    )

    c2.metric(
        "⏳ Pending",
        pending
    )

    c3.metric(
        "✅ Reviewed",
        reviewed
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

    st.subheader("🕒 Recent Assessments")

    for record in reversed(records[-5:]):

        with st.container():

            if record[7] == "High":

                st.error(
                        f"🚨 {record[1]} | Risk: {record[7]} | Status: {record[8]}"
                    )

            elif record[7] == "Medium":

                st.warning(
                            f"⚠ {record[1]} | Risk: {record[7]} | Status: {record[8]}"
                        )

            else:

                st.success(
                        f"✅ {record[1]} | Risk: {record[7]} | Status: {record[8]}"
                    )

            st.write(
                f"🩺 Symptoms: {record[2]}"
            )

            st.divider()
    st.subheader("📝 Recent Patient Self Reports")

    reports = get_patient_reports()

    for report in reports[:5]:

        st.info(
                f"""
        Patient: {report[1]}

        Risk: {report[5]}

        Status: {report[6]}
        """
            )

elif menu == "💊 Care Reminders":

    st.header("📅 Reminder Center")

    patients = get_patients()

    col1, col2 = st.columns(2)

    col1.metric(
        "💊 Medication Reminders",
        len(patients)
    )

    col2.metric(
        "📅 Appointment Reminders",
        len(patients)
    )

    st.markdown("---")

    st.subheader("📋 Patients Pending Follow-Up")

    if not patients:

        st.info(
            "No patients available."
        )

    else:

        for patient in patients:

            with st.container():

                st.info(
                    f"""
👤 Patient: {patient[1]}

📞 Phone: {patient[3]}

💊 Medication: {patient[6]}

📅 Follow-Up Date: {patient[7]}
"""
                )


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

        📝 Recovery Check-In

        Please submit your recovery status using the Patient Portal.

        Report:
        • Current symptoms
        • Fever status
        • Medication adherence

        This helps our healthcare team monitor your recovery.

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

        📝 Before your appointment, please submit your latest recovery report through the Patient Portal.

        This helps our healthcare team review your condition in advance.

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

    st.markdown("---")

elif menu == "🚨 Alert Center":

    st.header("🚨 Healthcare Alert Center")

    records = get_followups()

    high_risk = [
        r for r in records
        if r[7] == "High" and r[8] != "Reviewed"
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

                    st.write(
                        f"📌 Status: {record[8]}"
                    )

                st.warning(
                    "Immediate healthcare staff review recommended."
                )

                action1, action2, action3 = st.columns(3)

                with action1:

                    if st.button(
                        f"📩 Notify Doctor - {record[0]}"
                    ):

                        send_doctor_alert(
                            f"""
HIGH RISK PATIENT

Patient: {record[1]}
Symptoms: {record[2]}
Risk: {record[7]}
"""
                        )

                        st.success(
                            "Doctor notification sent."
                        )

                with action2:

                    if st.button(
                        f"📞 Call Patient - {record[0]}"
                    ):

                        st.info(
                            "Voice call workflow initiated."
                        )

                with action3:

                    if st.button(
                        f"✅ Mark Reviewed - {record[0]}"
                    ):

                        update_followup_status(
                            record[0],
                            "Reviewed"
                        )

                        st.success(
                            "Patient marked as reviewed."
                        )

                        st.rerun()

                st.divider()

elif menu == "🤖 Follow-Up Agent":

    records = get_followups()
    reports = get_patient_reports()

    st.header("🤖 Follow-Up Agent")

    st.subheader("⚙️ Agent Status")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "👥 Patients Monitored",
        len(get_patients())
    )

    col2.metric(
        "🚨 High-Risk Cases",
        len(
            [
                r for r in records
                if r[7] == "High"
                and r[8] != "Reviewed"
            ]
        )
    )

    col3.metric(
        "📝 Reports Received",
        len(reports)
    )

    st.info(
        """
The Healthcare Follow-Up Agent continuously monitors discharged patients,
supports medication adherence, tracks recovery progress,
and escalates high-risk cases to healthcare staff.
"""
    )

    st.subheader("📋 Recent Agent Activity")

    st.success(
        "✅ Welcome messages are sent automatically after patient registration."
    )

    st.success(
        "✅ High-risk patients are automatically escalated."
    )

    st.success(
        "✅ Reminder engine available through agent_scheduler.py."
    )

    st.markdown("---")

    patient_names = get_patient_names()

    if not patient_names:

        st.warning(
            "No registered patients found."
        )

        st.stop()

    patient_name = st.selectbox(
        "Select Patient",
        patient_names
    )

    patient = get_patient_by_name(
        patient_name
    )

    latest_followup = get_latest_followup(
        patient_name
    )

    if patient:

        st.info(
            f"📞 Phone: {patient[3]}"
        )

        st.info(
            f"💊 Medication: {patient[6]}"
        )

        st.info(
            f"📅 Follow-Up Date: {patient[7]}"
        )

        st.subheader(
            "📋 Latest Patient Status"
        )

        if latest_followup:

            st.warning(
                f"""
Risk Level: {latest_followup[7]}

Status: {latest_followup[8]}

Symptoms: {latest_followup[2]}
"""
            )

        else:

            st.info(
                "No follow-up assessments available yet."
            )

        if st.button(
            "📩 Generate & Send Follow-Up Message"
        ):

            message = generate_followup_message(
                patient[1],
                patient[6],
                patient[7]
            )

            st.subheader(
                "Generated Message"
            )

            st.write(
                message
            )

            sid = send_whatsapp(
                patient[3],
                message
            )

            st.success(
                "✅ Personalized outreach sent successfully!"
            )

            st.write(
                f"Message SID: {sid}"
            )

elif menu == "👨‍⚕️ Doctor Portal":
    tab1, tab2, tab3 = st.tabs([
        "Register Doctor",
        "Doctor Login",
        "Doctor Dashboard"
    ])
    with tab1:
        st.subheader("Doctor Registration")

        doctor_name = st.text_input("Doctor Name")
        specialization = st.text_input("Specialization")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        phone = st.text_input("Phone")

        if st.button("Register Doctor"):
            add_doctor(
                doctor_name,
                specialization,
                email,
                password,
                phone
            )
            st.success("Doctor Registered Successfully")

    with tab2:
        st.subheader("Doctor Login")

        email = st.text_input("Login Email")
        password = st.text_input(
            "Login Password",
            type="password"
        )

        if st.button("Login"):
            doctor = doctor_login(
                email,
                password
            )

            if doctor:
                st.session_state["doctor"] = doctor
                st.success(
                    f"Welcome Dr. {doctor['name']}"
                )
            else:
                st.error(
                    "Invalid Credentials"
                )
    with tab3:
    
        st.subheader("Doctor Dashboard")

        if "doctor" not in st.session_state:
            st.warning("Please Login First")

        else:
            doctor = st.session_state["doctor"]

            patients = get_patients_by_doctor(
                doctor["id"]
            )

            st.success(
                f"Logged in as Dr. {doctor['name']}"
            )

            st.write(
                "Specialization:",
                doctor["specialization"]
            )

            st.write(
                "Email:",
                doctor["email"]
            )

            st.write(
                "Phone:",
                doctor["phone"]
            )

            st.subheader("Assigned Patients")

            if patients:

                for patient in patients:

                    st.container()

                    st.markdown(
                        f"""
            ### 👤 {patient['name']}

            **Condition:** {patient['condition']}

            **Follow-up Date:** {patient['followup_date']}

            **Phone:** {patient['phone']}
            """
                    )

                    st.divider()

            else:

                st.info("No patients assigned.")
            
            