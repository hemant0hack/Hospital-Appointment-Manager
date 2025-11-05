# app.py
import streamlit as st
from datetime import datetime
import pandas as pd
from database import HospitalDatabase

# Initialize database
@st.cache_resource
def get_database():
    return HospitalDatabase()

db = get_database()

def get_current_datetime():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def main():
    st.set_page_config(
        page_title="Hospital Appointment Manager",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better spacing and readability
    st.markdown("""
        <style>
        .main > div {
            padding: 0;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2em;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
        }
        div[data-testid="stToolbar"] {
            display: none;
        }
        .main .block-container {
            padding-top: 0;
            padding-bottom: 2em;
        }
        header {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

    # Main header centered
    st.markdown("""
        <h1 style='text-align: center; padding: 0; margin: 0 0 0.5em 0'>
            🏥 Hospital Appointment Manager
        </h1>
    """, unsafe_allow_html=True)
    
    # Navigation menu below header
    menu_options = {
        "Dashboard": "📊 Dashboard",
        "Patients Management": "👥 Patients",
        "Doctors Management": "👨‍⚕️ Doctors",
        "Appointments Management": "📅 Appointments",
        "Reset All Data": "🔄 Reset Data"
    }
    choice = st.radio(
        "",
        list(menu_options.keys()),
        format_func=lambda x: menu_options[x],
        horizontal=True,
        key="main_navigation"
    )
    st.markdown("<hr style='margin: 0.5em 0 2em 0'>", unsafe_allow_html=True)
    
    # Load data from database
    patients = db.get_all_patients()
    doctors = db.get_all_doctors()
    appointments = db.get_all_appointments()
    
    # Dashboard
    if choice == "Dashboard":
        show_dashboard(patients, doctors, appointments)
    
    # Patients Management
    elif choice == "Patients Management":
        patients_management()
    
    # Doctors Management
    elif choice == "Doctors Management":
        doctors_management()
    
    # Appointments Management
    elif choice == "Appointments Management":
        appointments_management(patients, doctors)
    
    # Reset Data
    elif choice == "Reset All Data":
        reset_data()

def show_dashboard(patients, doctors, appointments):
    st.header("📊 Hospital Overview")
    
    # Stats cards with better visual presentation
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Total Patients",
            len(patients),
            help="Total number of registered patients in the system"
        )
    with col2:
        st.metric(
            "Total Doctors",
            len(doctors),
            help="Total number of registered doctors in the system"
        )
    with col3:
        st.metric(
            "Total Appointments",
            len(appointments),
            help="Total number of scheduled appointments"
        )
    
    st.markdown("---")
    
    # Recent Activity section with better organization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🆕 Recent Patients")
        if patients:
            recent_patients = patients[-5:] if len(patients) > 5 else patients
            for patient in reversed(recent_patients):
                with st.container():
                    st.markdown(f"""
                        **Patient:** {patient['name']}  
                        **ID:** {patient['id']}  
                        **Condition:** {patient['disease']}
                        """)
                    st.markdown("---")
        else:
            st.info("👋 No patients registered yet. Add your first patient from the Patients Management section.")
    
    with col2:
        st.subheader("📅 Recent Appointments")
        if appointments:
            recent_appointments = appointments[-5:] if len(appointments) > 5 else appointments
            for appointment in reversed(recent_appointments):
                with st.container():
                    st.markdown(f"""
                        **Patient:** {appointment['patientName']}  
                        **Doctor:** {appointment['doctorName']}  
                        **Date:** {appointment['appointmentDateTime']}
                        """)
                    st.markdown("---")
        else:
            st.info("📝 No appointments scheduled yet. Schedule one from the Appointments Management section.")

def patients_management():
    st.header("👥 Patients Management")
    st.caption("Add, view, edit, or remove patient records")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "➕ Add Patient",
        "📋 View All",
        "✏️ Edit Patient",
        "🔍 Search Patient",
        "❌ Delete Patient"
    ])
    
    with tab1:
        st.subheader("Add New Patient")
        with st.form("add_patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                pid = st.text_input("Patient ID*")
                name = st.text_input("Patient Name*")
                age = st.number_input("Age", min_value=0, max_value=150, value=0)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            
            with col2:
                address = st.text_area("Address")
                disease = st.text_input("Disease*")
                referred_by = st.text_input("Referred By")
            
            if st.form_submit_button("Add Patient"):
                if pid and name and disease:
                    # Check if patient ID already exists
                    existing_patient = db.get_patient_by_id(pid)
                    if existing_patient:
                        st.error("Patient ID already exists! Please use a different ID.")
                    else:
                        patient_data = {
                            "id": pid,
                            "name": name,
                            "age": age,
                            "gender": gender,
                            "address": address,
                            "disease": disease,
                            "REFERRED_BY": referred_by,
                            "admissionDateTime": get_current_datetime(),
                        }
                        db.add_patient(patient_data)
                        st.success("Patient added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")
    
    with tab2:
        st.subheader("All Patients")
        patients = db.get_all_patients()
        if patients:
            patients_df = pd.DataFrame(patients)
            st.dataframe(patients_df, use_container_width=True)
        else:
            st.info("No patients found")
    
    with tab3:
        st.subheader("Edit Patient")
        patients = db.get_all_patients()
        if patients:
            patient_ids = [p['id'] for p in patients]
            selected_pid = st.selectbox("Select Patient ID to edit", patient_ids)
            
            if selected_pid:
                patient = db.get_patient_by_id(selected_pid)
                
                with st.form("edit_patient_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input("Name", value=patient['name'])
                        new_age = st.number_input("Age", value=patient['age'])
                        new_gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                                                index=["Male", "Female", "Other"].index(patient['gender']))
                    
                    with col2:
                        new_address = st.text_area("Address", value=patient['address'])
                        new_disease = st.text_input("Disease", value=patient['disease'])
                        new_referred_by = st.text_input("Referred By", value=patient['REFERRED_BY'])
                    
                    if st.form_submit_button("Update Patient"):
                        updated_data = {
                            "name": new_name,
                            "age": new_age,
                            "gender": new_gender,
                            "address": new_address,
                            "disease": new_disease,
                            "REFERRED_BY": new_referred_by,
                            "admissionDateTime": get_current_datetime(),
                        }
                        db.update_patient(selected_pid, updated_data)
                        st.success("Patient updated successfully!")
                        st.rerun()
        else:
            st.info("No patients available to edit")
    
    with tab4:
        st.subheader("View Patient by ID")
        patients = db.get_all_patients()
        if patients:
            patient_ids = [p['id'] for p in patients]
            selected_pid = st.selectbox("Select Patient ID", patient_ids)
            
            if selected_pid:
                patient = db.get_patient_by_id(selected_pid)
                st.json(patient)
        else:
            st.info("No patients available")
    
    with tab5:
        st.subheader("Delete Patient")
        patients = db.get_all_patients()
        if patients:
            patient_ids = [p['id'] for p in patients]
            selected_pid = st.selectbox("Select Patient ID to delete", patient_ids, key="delete_patient")
            
            if selected_pid:
                patient = db.get_patient_by_id(selected_pid)
                st.warning(f"Are you sure you want to delete patient: {patient['name']} (ID: {patient['id']})?")
                
                if st.button("Confirm Delete"):
                    db.delete_patient(selected_pid)
                    st.success("Patient deleted successfully!")
                    st.rerun()
        else:
            st.info("No patients available to delete")

def doctors_management():
    st.header("👨‍⚕️ Doctors Management")
    st.caption("Add, view, edit, or remove doctor records")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "➕ Add Doctor",
        "📋 View All",
        "✏️ Edit Doctor",
        "🔍 Search Doctor",
        "❌ Delete Doctor"
    ])
    
    with tab1:
        st.subheader("Add New Doctor")
        with st.form("add_doctor_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                did = st.text_input("Doctor ID*")
                name = st.text_input("Doctor Name*")
            
            with col2:
                specialization = st.text_input("Specialization*")
                experience = st.number_input("Experience (years)", min_value=0, max_value=50, value=0)
            
            if st.form_submit_button("Add Doctor"):
                if did and name and specialization:
                    # Check if doctor ID already exists
                    existing_doctor = db.get_doctor_by_id(did)
                    if existing_doctor:
                        st.error("Doctor ID already exists! Please use a different ID.")
                    else:
                        doctor_data = {
                            "id": did,
                            "name": name,
                            "specialization": specialization,
                            "experience": experience,
                        }
                        db.add_doctor(doctor_data)
                        st.success("Doctor added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")
    
    with tab2:
        st.subheader("All Doctors")
        doctors = db.get_all_doctors()
        if doctors:
            doctors_df = pd.DataFrame(doctors)
            st.dataframe(doctors_df, use_container_width=True)
        else:
            st.info("No doctors found")
    
    with tab3:
        st.subheader("Edit Doctor")
        doctors = db.get_all_doctors()
        if doctors:
            doctor_ids = [d['id'] for d in doctors]
            selected_did = st.selectbox("Select Doctor ID to edit", doctor_ids)
            
            if selected_did:
                doctor = db.get_doctor_by_id(selected_did)
                
                with st.form("edit_doctor_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input("Name", value=doctor['name'])
                        new_specialization = st.text_input("Specialization", value=doctor['specialization'])
                    
                    with col2:
                        new_experience = st.number_input("Experience (years)", value=doctor['experience'])
                    
                    if st.form_submit_button("Update Doctor"):
                        updated_data = {
                            "name": new_name,
                            "specialization": new_specialization,
                            "experience": new_experience,
                        }
                        db.update_doctor(selected_did, updated_data)
                        st.success("Doctor updated successfully!")
                        st.rerun()
        else:
            st.info("No doctors available to edit")
    
    with tab4:
        st.subheader("View Doctor by ID")
        doctors = db.get_all_doctors()
        if doctors:
            doctor_ids = [d['id'] for d in doctors]
            selected_did = st.selectbox("Select Doctor ID", doctor_ids, key="view_doctor")
            
            if selected_did:
                doctor = db.get_doctor_by_id(selected_did)
                st.json(doctor)
        else:
            st.info("No doctors available")
    
    with tab5:
        st.subheader("Delete Doctor")
        doctors = db.get_all_doctors()
        if doctors:
            doctor_ids = [d['id'] for d in doctors]
            selected_did = st.selectbox("Select Doctor ID to delete", doctor_ids, key="delete_doctor")
            
            if selected_did:
                doctor = db.get_doctor_by_id(selected_did)
                st.warning(f"Are you sure you want to delete doctor: {doctor['name']} (ID: {doctor['id']})?")
                
                if st.button("Confirm Delete"):
                    db.delete_doctor(selected_did)
                    st.success("Doctor deleted successfully!")
                    st.rerun()
        else:
            st.info("No doctors available to delete")

def appointments_management(patients, doctors):
    st.header("📅 Appointments Management")
    st.caption("Schedule, view, modify, or cancel appointments")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "➕ New Appointment",
        "📋 View All",
        "✏️ Edit Appointment",
        "🔍 Search Appointment",
        "❌ Cancel Appointment"
    ])
    
    with tab1:
        st.subheader("Add New Appointment")
        with st.form("add_appointment_form"):
            aid = st.text_input("Appointment ID*")
            
            # Get available patients and doctors
            patient_names = [p['name'] for p in patients]
            doctor_names = [d['name'] for d in doctors]
            
            col1, col2 = st.columns(2)
            
            with col1:
                if patient_names:
                    patient_name = st.selectbox("Patient Name*", patient_names)
                else:
                    st.warning("No patients available. Please add patients first.")
                    patient_name = ""
            
            with col2:
                if doctor_names:
                    doctor_name = st.selectbox("Doctor Name*", doctor_names)
                else:
                    st.warning("No doctors available. Please add doctors first.")
                    doctor_name = ""
            
            # Date and time selection
            col1, col2 = st.columns(2)
            with col1:
                appointment_date = st.date_input(
                    "Appointment Date*",
                    help="Select the date for the appointment"
                )
            with col2:
                appointment_time = st.time_input(
                    "Appointment Time*",
                    help="Select the time (appointments are in 30-minute slots)"
                )
            
            if st.form_submit_button("Add Appointment"):
                if aid and patient_name and doctor_name and appointment_date and appointment_time:
                    # Format the appointment datetime
                    appointment_datetime = datetime.combine(
                        appointment_date,
                        appointment_time
                    ).strftime("%d-%m-%Y %H:%M:%S")
                    
                    # Check if appointment ID already exists
                    existing_appointment = db.get_appointment_by_id(aid)
                    if existing_appointment:
                        st.error("Appointment ID already exists! Please use a different ID.")
                    else:
                        appointment_data = {
                            "id": aid,
                            "patientName": patient_name,
                            "doctorName": doctor_name,
                            "appointmentDateTime": appointment_datetime,
                        }
                        db.add_appointment(appointment_data)
                        st.success("Appointment added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")
    
    with tab2:
        st.subheader("All Appointments")
        appointments = db.get_all_appointments()
        
        if appointments:
            # Add filter by date
            filter_date = st.date_input(
                "Filter by Date",
                help="Show appointments for a specific date"
            )
            
            # Filter appointments by selected date
            filtered_appointments = []
            for apt in appointments:
                apt_date = datetime.strptime(apt['appointmentDateTime'], "%d-%m-%Y %H:%M:%S").date()
                if apt_date == filter_date:
                    filtered_appointments.append(apt)
            
            if filtered_appointments:
                appointments_df = pd.DataFrame(filtered_appointments)
                
                # Format the datetime column for better display
                appointments_df['Time'] = pd.to_datetime(appointments_df['appointmentDateTime']).dt.strftime('%I:%M %p')
                appointments_df = appointments_df.rename(columns={
                    'patientName': 'Patient',
                    'doctorName': 'Doctor',
                    'id': 'ID'
                })
                appointments_df = appointments_df[['ID', 'Patient', 'Doctor', 'Time']]
                
                st.dataframe(appointments_df, use_container_width=True)
            else:
                st.info(f"No appointments found for {filter_date.strftime('%d-%m-%Y')}")
        else:
            st.info("No appointments found")
    
    with tab3:
        st.subheader("Edit Appointment")
        appointments = db.get_all_appointments()
        patients = db.get_all_patients()
        doctors = db.get_all_doctors()
        
        if appointments:
            appointment_ids = [a['id'] for a in appointments]
            selected_aid = st.selectbox("Select Appointment ID to edit", appointment_ids)
            
            if selected_aid:
                appointment = db.get_appointment_by_id(selected_aid)
                
                with st.form("edit_appointment_form"):
                    # Get available patients and doctors
                    patient_names = [p['name'] for p in patients]
                    doctor_names = [d['name'] for d in doctors]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if patient_names:
                            new_patient_name = st.selectbox("Patient Name", patient_names, 
                                                          index=patient_names.index(appointment['patientName']) if appointment['patientName'] in patient_names else 0)
                        else:
                            st.warning("No patients available")
                            new_patient_name = ""
                    
                    with col2:
                        if doctor_names:
                            new_doctor_name = st.selectbox("Doctor Name", doctor_names,
                                                         index=doctor_names.index(appointment['doctorName']) if appointment['doctorName'] in doctor_names else 0)
                        else:
                            st.warning("No doctors available")
                            new_doctor_name = ""
                    
                    if st.form_submit_button("Update Appointment"):
                        updated_data = {
                            "patientName": new_patient_name,
                            "doctorName": new_doctor_name,
                            "appointmentDateTime": get_current_datetime(),
                        }
                        db.update_appointment(selected_aid, updated_data)
                        st.success("Appointment updated successfully!")
                        st.rerun()
        else:
            st.info("No appointments available to edit")
    
    with tab4:
        st.subheader("View Appointment by ID")
        appointments = db.get_all_appointments()
        if appointments:
            appointment_ids = [a['id'] for a in appointments]
            selected_aid = st.selectbox("Select Appointment ID", appointment_ids, key="view_appointment")
            
            if selected_aid:
                appointment = db.get_appointment_by_id(selected_aid)
                st.json(appointment)
        else:
            st.info("No appointments available")
    
    with tab5:
        st.subheader("Delete Appointment")
        appointments = db.get_all_appointments()
        if appointments:
            appointment_ids = [a['id'] for a in appointments]
            selected_aid = st.selectbox("Select Appointment ID to delete", appointment_ids, key="delete_appointment")
            
            if selected_aid:
                appointment = db.get_appointment_by_id(selected_aid)
                st.warning(f"Are you sure you want to delete appointment: {appointment['patientName']} with {appointment['doctorName']}?")
                
                if st.button("Confirm Delete"):
                    db.delete_appointment(selected_aid)
                    st.success("Appointment deleted successfully!")
                    st.rerun()
        else:
            st.info("No appointments available to delete")

def reset_data():
    st.header("🔄 Reset Database")
    st.caption("Clear all data from the system")
    
    st.warning("⚠️ Warning: This action will permanently delete all data!")
    
    with st.expander("Click to show reset options"):
        st.error("""
            This will delete:
            - All patient records
            - All doctor records
            - All appointment schedules
            
            This action CANNOT be undone. Please make sure you have backed up any important data.
        """)
        
        confirm_text = st.text_input(
            "Type 'RESET' to confirm deletion of all data",
            help="This is a safety measure to prevent accidental data loss"
        )
        
        if confirm_text == "RESET" and st.button("Reset All Data", type="primary"):
            db.reset_all_data()
            st.success("✅ All data has been reset successfully!")
            st.rerun()

if __name__ == "__main__":
    main()