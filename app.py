import streamlit as st
from datetime import datetime
import pandas as pd

# Initialize session state for data persistence
if 'patients' not in st.session_state:
    st.session_state.patients = []
if 'doctors' not in st.session_state:
    st.session_state.doctors = []
if 'appointments' not in st.session_state:
    st.session_state.appointments = []

def get_current_datetime():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def main():
    st.set_page_config(
        page_title="Hospital Appointment Manager",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🏥 Hospital Appointment Manager")
    st.markdown("---")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    menu_options = [
        "Dashboard",
        "Patients Management", 
        "Doctors Management",
        "Appointments Management",
        "Reset All Data"
    ]
    choice = st.sidebar.selectbox("Select Module", menu_options)
    
    # Dashboard
    if choice == "Dashboard":
        show_dashboard()
    
    # Patients Management
    elif choice == "Patients Management":
        patients_management()
    
    # Doctors Management
    elif choice == "Doctors Management":
        doctors_management()
    
    # Appointments Management
    elif choice == "Appointments Management":
        appointments_management()
    
    # Reset Data
    elif choice == "Reset All Data":
        reset_data()

def show_dashboard():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Patients", len(st.session_state.patients))
    
    with col2:
        st.metric("Total Doctors", len(st.session_state.doctors))
    
    with col3:
        st.metric("Total Appointments", len(st.session_state.appointments))
    
    st.markdown("---")
    
    # Recent Activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent Patients")
        if st.session_state.patients:
            recent_patients = st.session_state.patients[-5:] if len(st.session_state.patients) > 5 else st.session_state.patients
            for patient in reversed(recent_patients):
                st.write(f"**{patient['name']}** (ID: {patient['id']}) - {patient['disease']}")
        else:
            st.info("No patients registered yet")
    
    with col2:
        st.subheader("Recent Appointments")
        if st.session_state.appointments:
            recent_appointments = st.session_state.appointments[-5:] if len(st.session_state.appointments) > 5 else st.session_state.appointments
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
                    st.session_state.patients.append(patient_data)
                    st.success("Patient added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")
    
    with tab2:
        st.subheader("All Patients")
        if st.session_state.patients:
            patients_df = pd.DataFrame(st.session_state.patients)
            st.dataframe(patients_df, use_container_width=True)
        else:
            st.info("No patients found")
    
    with tab3:
        st.subheader("Edit Patient")
        if st.session_state.patients:
            patient_ids = [p['id'] for p in st.session_state.patients]
            selected_pid = st.selectbox("Select Patient ID to edit", patient_ids)
            
            if selected_pid:
                patient_idx = next(i for i, p in enumerate(st.session_state.patients) if p['id'] == selected_pid)
                patient = st.session_state.patients[patient_idx]
                
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
                        st.session_state.patients[patient_idx].update({
                            "name": new_name,
                            "age": new_age,
                            "gender": new_gender,
                            "address": new_address,
                            "disease": new_disease,
                            "REFERRED_BY": new_referred_by,
                            "admissionDateTime": get_current_datetime(),
                        })
                        st.success("Patient updated successfully!")
                        st.rerun()
        else:
            st.info("No patients available to edit")
    
    with tab4:
        st.subheader("View Patient by ID")
        if st.session_state.patients:
            patient_ids = [p['id'] for p in st.session_state.patients]
            selected_pid = st.selectbox("Select Patient ID", patient_ids)
            
            if selected_pid:
                patient = next(p for p in st.session_state.patients if p['id'] == selected_pid)
                st.json(patient)
        else:
            st.info("No patients available")
    
    with tab5:
        st.subheader("Delete Patient")
        if st.session_state.patients:
            patient_ids = [p['id'] for p in st.session_state.patients]
            selected_pid = st.selectbox("Select Patient ID to delete", patient_ids, key="delete_patient")
            
            if selected_pid:
                patient = next(p for p in st.session_state.patients if p['id'] == selected_pid)
                st.warning(f"Are you sure you want to delete patient: {patient['name']} (ID: {patient['id']})?")
                
                if st.button("Confirm Delete"):
                    st.session_state.patients = [p for p in st.session_state.patients if p['id'] != selected_pid]
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
                    doctor_data = {
                        "id": did,
                        "name": name,
                        "specialization": specialization,
                        "experience": experience,
                    }
                    st.session_state.doctors.append(doctor_data)
                    st.success("Doctor added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")
    
    with tab2:
        st.subheader("All Doctors")
        if st.session_state.doctors:
            doctors_df = pd.DataFrame(st.session_state.doctors)
            st.dataframe(doctors_df, use_container_width=True)
        else:
            st.info("No doctors found")
    
    with tab3:
        st.subheader("Edit Doctor")
        if st.session_state.doctors:
            doctor_ids = [d['id'] for d in st.session_state.doctors]
            selected_did = st.selectbox("Select Doctor ID to edit", doctor_ids)
            
            if selected_did:
                doctor_idx = next(i for i, d in enumerate(st.session_state.doctors) if d['id'] == selected_did)
                doctor = st.session_state.doctors[doctor_idx]
                
                with st.form("edit_doctor_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input("Name", value=doctor['name'])
                        new_specialization = st.text_input("Specialization", value=doctor['specialization'])
                    
                    with col2:
                        new_experience = st.number_input("Experience (years)", value=doctor['experience'])
                    
                    if st.form_submit_button("Update Doctor"):
                        st.session_state.doctors[doctor_idx].update({
                            "name": new_name,
                            "specialization": new_specialization,
                            "experience": new_experience,
                        })
                        st.success("Doctor updated successfully!")
                        st.rerun()
        else:
            st.info("No doctors available to edit")
    
    with tab4:
        st.subheader("View Doctor by ID")
        if st.session_state.doctors:
            doctor_ids = [d['id'] for d in st.session_state.doctors]
            selected_did = st.selectbox("Select Doctor ID", doctor_ids, key="view_doctor")
            
            if selected_did:
                doctor = next(d for d in st.session_state.doctors if d['id'] == selected_did)
                st.json(doctor)
        else:
            st.info("No doctors available")
    
    with tab5:
        st.subheader("Delete Doctor")
        if st.session_state.doctors:
            doctor_ids = [d['id'] for d in st.session_state.doctors]
            selected_did = st.selectbox("Select Doctor ID to delete", doctor_ids, key="delete_doctor")
            
            if selected_did:
                doctor = next(d for d in st.session_state.doctors if d['id'] == selected_did)
                st.warning(f"Are you sure you want to delete doctor: {doctor['name']} (ID: {doctor['id']})?")
                
                if st.button("Confirm Delete"):
                    st.session_state.doctors = [d for d in st.session_state.doctors if d['id'] != selected_did]
                    st.success("Doctor deleted successfully!")
                    st.rerun()
        else:
            st.info("No doctors available to delete")

def appointments_management():
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
            patient_names = [p['name'] for p in st.session_state.patients]
            doctor_names = [d['name'] for d in st.session_state.doctors]
            
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
                    appointment_data = {
                        "id": aid,
                        "patientName": patient_name,
                        "doctorName": doctor_name,
                        "appointmentDateTime": get_current_datetime(),
                    }
                    st.session_state.appointments.append(appointment_data)
                    st.success("Appointment added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")
    
    with tab2:
        st.subheader("All Appointments")
        if st.session_state.appointments:
            appointments_df = pd.DataFrame(st.session_state.appointments)
            st.dataframe(appointments_df, use_container_width=True)
        else:
            st.info("No appointments found")
    
    with tab3:
        st.subheader("Edit Appointment")
        if st.session_state.appointments:
            appointment_ids = [a['id'] for a in st.session_state.appointments]
            selected_aid = st.selectbox("Select Appointment ID to edit", appointment_ids)
            
            if selected_aid:
                appointment_idx = next(i for i, a in enumerate(st.session_state.appointments) if a['id'] == selected_aid)
                appointment = st.session_state.appointments[appointment_idx]
                
                with st.form("edit_appointment_form"):
                    # Get available patients and doctors
                    patient_names = [p['name'] for p in st.session_state.patients]
                    doctor_names = [d['name'] for d in st.session_state.doctors]
                    
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
                        st.session_state.appointments[appointment_idx].update({
                            "patientName": new_patient_name,
                            "doctorName": new_doctor_name,
                            "appointmentDateTime": get_current_datetime(),
                        })
                        st.success("Appointment updated successfully!")
                        st.rerun()
        else:
            st.info("No appointments available to edit")
    
    with tab4:
        st.subheader("View Appointment by ID")
        if st.session_state.appointments:
            appointment_ids = [a['id'] for a in st.session_state.appointments]
            selected_aid = st.selectbox("Select Appointment ID", appointment_ids, key="view_appointment")
            
            if selected_aid:
                appointment = next(a for a in st.session_state.appointments if a['id'] == selected_aid)
                st.json(appointment)
        else:
            st.info("No appointments available")
    
    with tab5:
        st.subheader("Delete Appointment")
        if st.session_state.appointments:
            appointment_ids = [a['id'] for a in st.session_state.appointments]
            selected_aid = st.selectbox("Select Appointment ID to delete", appointment_ids, key="delete_appointment")
            
            if selected_aid:
                appointment = next(a for a in st.session_state.appointments if a['id'] == selected_aid)
                st.warning(f"Are you sure you want to delete appointment: {appointment['patientName']} with {appointment['doctorName']}?")
                
                if st.button("Confirm Delete"):
                    st.session_state.appointments = [a for a in st.session_state.appointments if a['id'] != selected_aid]
                    st.success("Appointment deleted successfully!")
                    st.rerun()
        else:
            st.info("No appointments available to delete")

def reset_data():
    st.header("🔄 Reset All Data")
    
    st.warning("⚠️ This action cannot be undone!")
    st.error("All patient, doctor, and appointment data will be permanently deleted.")
    
    if st.button("Reset All Data", type="primary"):
        st.session_state.patients = []
        st.session_state.doctors = []
        st.session_state.appointments = []
        st.success("All data has been reset successfully!")
        st.rerun()

if __name__ == "__main__":
    main()