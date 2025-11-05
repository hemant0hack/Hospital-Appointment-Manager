# app.py
import streamlit as st
from datetime import datetime
import pandas as pd
from database import HospitalDatabase

# Initialize database and inject custom CSS
def inject_custom_css():
    st.markdown("""
        <style>
            .stApp {
                max-width: 1200px;
                margin: 0 auto;
            }
            .stMetric {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 10px;
            }
            .stTabs [data-baseweb="tab"] {
                padding: 10px 20px;
                background-color: #f8f9fa;
            }
            .form-container {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .success-alert {
                padding: 10px;
                background-color: #d4edda;
                color: #155724;
                border-radius: 4px;
                margin: 10px 0;
            }
            .error-alert {
                padding: 10px;
                background-color: #f8d7da;
                color: #721c24;
                border-radius: 4px;
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def get_database():
    try:
        db = HospitalDatabase()
        # Test database connection
        db.get_connection().close()
        return db
    except Exception as e:
        st.error(f"Database initialization error: {str(e)}")
        return None

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
    
    if db is None:
        st.error("Failed to initialize the database. Please check the database connection.")
        st.stop()
        
    inject_custom_css()
    
    # Header
    col1, col2 = st.columns([3,1])
    with col1:
        st.title("🏥 Hospital Appointment Manager")
    with col2:
        st.caption(f"Last Updated: {get_current_datetime()}")
    st.markdown("---")
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        menu_options = [
            "Dashboard",
            "Patients Management", 
            "Doctors Management",
            "Appointments Management",
            "Reset All Data"
        ]
        choice = st.selectbox("Select Module", menu_options)
    
    # Load data from database with error handling
    try:
        patients = db.get_all_patients()
        doctors = db.get_all_doctors()
        appointments = db.get_all_appointments()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        patients, doctors, appointments = [], [], []
    
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
    # Summary metrics with icons
    st.subheader("📊 Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👥 Total Patients", len(patients))
    
    with col2:
        st.metric("👨‍⚕️ Total Doctors", len(doctors))
    
    with col3:
        st.metric("📅 Total Appointments", len(appointments))
    
    st.markdown("---")
    
    # Recent Activity with better formatting
    st.subheader("📋 Recent Activity")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent Patients")
        if patients:
            recent_patients = patients[-5:] if len(patients) > 5 else patients
            for patient in reversed(recent_patients):
                st.write(f"**{patient['name']}** (ID: {patient['id']}) - {patient['disease']}")
        else:
            st.info("No patients registered yet")
    
    with col2:
        st.subheader("Recent Appointments")
        if appointments:
            recent_appointments = appointments[-5:] if len(appointments) > 5 else appointments
            for appointment in reversed(recent_appointments):
                st.write(f"**{appointment['patientName']}** with **{appointment['doctorName']}**")
        else:
            st.info("No appointments scheduled yet")

def patients_management():
    st.header("👥 Patients Management")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Add Patient", "View All Patients", "Edit Patient", 
        "View Patient by ID", "Delete Patient"
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
        try:
            patients = db.get_all_patients()
            if patients:
                patients_df = pd.DataFrame(patients)
                
                # Add filters
                col1, col2, col3 = st.columns(3)
                with col1:
                    name_filter = st.text_input("🔍 Search by name")
                with col2:
                    gender_filter = st.selectbox("Filter by gender", ["All", "Male", "Female", "Other"])
                with col3:
                    sort_by = st.selectbox("Sort by", ["Admission Date", "Name", "Age"])
                
                # Apply filters
                filtered_df = patients_df.copy()
                if name_filter:
                    filtered_df = filtered_df[filtered_df['name'].str.contains(name_filter, case=False, na=False)]
                if gender_filter != "All":
                    filtered_df = filtered_df[filtered_df['gender'] == gender_filter]
                
                # Apply sorting
                if sort_by == "Admission Date":
                    filtered_df = filtered_df.sort_values('admissionDateTime', ascending=False)
                elif sort_by == "Name":
                    filtered_df = filtered_df.sort_values('name')
                elif sort_by == "Age":
                    filtered_df = filtered_df.sort_values('age', ascending=False)
                
                # Show results count
                st.caption(f"Showing {len(filtered_df)} of {len(patients_df)} patients")
                
                # Display the filtered dataframe
                st.dataframe(
                    filtered_df,
                    use_container_width=True,
                    column_config={
                        "name": "Name",
                        "age": st.column_config.NumberColumn("Age", format="%d years"),
                        "admissionDateTime": st.column_config.DatetimeColumn("Admission Date"),
                    }
                )
            else:
                st.info("No patients found")
        except Exception as e:
            st.error(f"Error loading patients: {str(e)}")
    
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
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Add Doctor", "View All Doctors", "Edit Doctor", 
        "View Doctor by ID", "Delete Doctor"
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
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Add Appointment", "View All Appointments", "Edit Appointment", 
        "View Appointment by ID", "Delete Appointment"
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
            
            if st.form_submit_button("Add Appointment"):
                if aid and patient_name and doctor_name:
                    # Check if appointment ID already exists
                    existing_appointment = db.get_appointment_by_id(aid)
                    if existing_appointment:
                        st.error("Appointment ID already exists! Please use a different ID.")
                    else:
                        appointment_data = {
                            "id": aid,
                            "patientName": patient_name,
                            "doctorName": doctor_name,
                            "appointmentDateTime": get_current_datetime(),
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
            appointments_df = pd.DataFrame(appointments)
            st.dataframe(appointments_df, use_container_width=True)
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
    st.header("🔄 Reset All Data")
    
    st.warning("⚠️ This action cannot be undone!")
    st.error("All patient, doctor, and appointment data will be permanently deleted from the database.")
    
    if st.button("Reset All Data", type="primary"):
        db.reset_all_data()
        st.success("All data has been reset successfully!")
        st.rerun()

if __name__ == "__main__":
    main()