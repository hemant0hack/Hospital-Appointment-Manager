# app.py
import streamlit as st
from datetime import datetime
import pandas as pd
from database import HospitalDatabase

# Initialize database
@st.cache_resource
def get_database():
    try:
        return HospitalDatabase()
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None

db = get_database()
if db is None:
    st.stop()

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    st.set_page_config(
        page_title="Hospital Manager",
        page_icon="🏥"
    )
    
    st.title("Hospital Manager")
    
    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Patients", "Doctors", "Appointments", "Reset Data"]
    )
    
    patients = db.get_all_patients()
    doctors = db.get_all_doctors()
    appointments = db.get_all_appointments()
    
    if menu == "Dashboard":
        show_dashboard(patients, doctors, appointments)
    elif menu == "Patients":
        patients_management()
    elif menu == "Doctors":
        doctors_management()
    elif menu == "Appointments":
        appointments_management(patients, doctors)
    elif menu == "Reset Data":
        reset_data()

def show_dashboard(patients, doctors, appointments):
    st.write("Summary")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Patients", len(patients))
    col2.metric("Doctors", len(doctors))
    col3.metric("Appointments", len(appointments))
    
    st.write("Recent Activity")
    
    if patients:
        recent_patients = patients[-5:] if len(patients) > 5 else patients
        st.write("Latest Patients:")
        for p in reversed(recent_patients):
            st.write(f"- {p['name']} ({p['disease']})")
    
    if appointments:
        recent_appointments = appointments[-5:] if len(appointments) > 5 else appointments
        st.write("Latest Appointments:")
        for a in reversed(recent_appointments):
            st.write(f"- {a['patientName']} with {a['doctorName']}")

def patients_management():
    st.header("Patients")
    
    tab1, tab2 = st.tabs(["Add/Edit", "View All"])
    
    with tab1:
        # Add new patient
        with st.form("patient_form"):
            st.write("Add New Patient")
            pid = st.text_input("ID*")
            name = st.text_input("Name*")
            age = st.number_input("Age", 0, 150)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            disease = st.text_input("Disease*")
            address = st.text_area("Address")
            referred_by = st.text_input("Referred By")
            
            if st.form_submit_button("Add Patient"):
                if pid and name and disease:
                    if db.get_patient_by_id(pid):
                        st.error("ID already exists")
                    else:
                        patient = {
                            "id": pid,
                            "name": name,
                            "age": age,
                            "gender": gender,
                            "address": address,
                            "disease": disease,
                            "REFERRED_BY": referred_by,
                            "admissionDateTime": get_current_datetime()
                        }
                        db.add_patient(patient)
                        st.success("Added successfully")
                        st.rerun()
                else:
                    st.error("Fill required fields (*)")
        
        # Edit/Delete existing patient
        st.write("Edit/Delete Patient")
        patients = db.get_all_patients()
        if patients:
            patient_ids = [p['id'] for p in patients]
            selected_pid = st.selectbox("Select Patient", patient_ids)
            
            if selected_pid:
                patient = db.get_patient_by_id(selected_pid)
                with st.form("edit_form"):
                    st.write(f"Editing Patient {selected_pid}")
                    name = st.text_input("Name", patient['name'])
                    age = st.number_input("Age", 0, 150, patient['age'])
                    gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                                        ["Male", "Female", "Other"].index(patient['gender']))
                    disease = st.text_input("Disease", patient['disease'])
                    address = st.text_area("Address", patient['address'])
                    referred_by = st.text_input("Referred By", patient['REFERRED_BY'])
                    
                    col1, col2 = st.columns(2)
                    update = col1.form_submit_button("Update")
                    delete = col2.form_submit_button("Delete")
                    
                    if update:
                        data = {
                            "name": name,
                            "age": age,
                            "gender": gender,
                            "address": address,
                            "disease": disease,
                            "REFERRED_BY": referred_by,
                            "admissionDateTime": get_current_datetime()
                        }
                        db.update_patient(selected_pid, data)
                        st.success("Updated")
                        st.rerun()
                    elif delete:
                        db.delete_patient(selected_pid)
                        st.success("Deleted")
                        st.rerun()
    
    with tab2:
        patients = db.get_all_patients()
        if patients:
            df = pd.DataFrame(patients)
            st.dataframe(df)

def doctors_management():
    st.header("Doctors")
    
    tab1, tab2 = st.tabs(["Add/Edit", "View All"])
    
    with tab1:
        # Add new doctor
        with st.form("doctor_form"):
            st.write("Add New Doctor")
            did = st.text_input("ID*")
            name = st.text_input("Name*")
            specialization = st.text_input("Specialization*")
            experience = st.number_input("Experience (years)", 0, 50)
            
            if st.form_submit_button("Add Doctor"):
                if did and name and specialization:
                    if db.get_doctor_by_id(did):
                        st.error("ID already exists")
                    else:
                        doctor = {
                            "id": did,
                            "name": name,
                            "specialization": specialization,
                            "experience": experience
                        }
                        db.add_doctor(doctor)
                        st.success("Added successfully")
                        st.rerun()
                else:
                    st.error("Fill required fields (*)")
        
        # Edit/Delete existing doctor
        st.write("Edit/Delete Doctor")
        doctors = db.get_all_doctors()
        if doctors:
            doctor_ids = [d['id'] for d in doctors]
            selected_did = st.selectbox("Select Doctor", doctor_ids)
            
            if selected_did:
                doctor = db.get_doctor_by_id(selected_did)
                with st.form("edit_form"):
                    st.write(f"Editing Doctor {selected_did}")
                    name = st.text_input("Name", doctor['name'])
                    specialization = st.text_input("Specialization", doctor['specialization'])
                    experience = st.number_input("Experience (years)", 0, 50, doctor['experience'])
                    
                    col1, col2 = st.columns(2)
                    update = col1.form_submit_button("Update")
                    delete = col2.form_submit_button("Delete")
                    
                    if update:
                        data = {
                            "name": name,
                            "specialization": specialization,
                            "experience": experience
                        }
                        db.update_doctor(selected_did, data)
                        st.success("Updated")
                        st.rerun()
                    elif delete:
                        db.delete_doctor(selected_did)
                        st.success("Deleted")
                        st.rerun()
    
    with tab2:
        doctors = db.get_all_doctors()
        if doctors:
            df = pd.DataFrame(doctors)
            st.dataframe(df)

def appointments_management(patients, doctors):
    st.header("Appointments")
    
    tab1, tab2 = st.tabs(["Add/Edit", "View All"])
    
    with tab1:
        # Add new appointment
        with st.form("appointment_form"):
            st.write("Add New Appointment")
            aid = st.text_input("ID*")
            patient_names = [p['name'] for p in patients] if patients else []
            doctor_names = [d['name'] for d in doctors] if doctors else []
            
            patient_name = st.selectbox("Patient*", patient_names) if patient_names else st.info("No patients available")
            doctor_name = st.selectbox("Doctor*", doctor_names) if doctor_names else st.info("No doctors available")
            
            if st.form_submit_button("Add Appointment"):
                if aid and patient_name and doctor_name:
                    if db.get_appointment_by_id(aid):
                        st.error("ID already exists")
                    else:
                        appointment = {
                            "id": aid,
                            "patientName": patient_name,
                            "doctorName": doctor_name,
                            "appointmentDateTime": get_current_datetime()
                        }
                        db.add_appointment(appointment)
                        st.success("Added successfully")
                        st.rerun()
                else:
                    st.error("Fill required fields (*)")
        
        # Edit/Delete existing appointment
        st.write("Edit/Delete Appointment")
        appointments = db.get_all_appointments()
        if appointments:
            appointment_ids = [a['id'] for a in appointments]
            selected_aid = st.selectbox("Select Appointment", appointment_ids)
            
            if selected_aid:
                appointment = db.get_appointment_by_id(selected_aid)
                patient_names = [p['name'] for p in patients] if patients else []
                doctor_names = [d['name'] for d in doctors] if doctors else []
                
                with st.form("edit_form"):
                    st.write(f"Editing Appointment {selected_aid}")
                    patient_name = st.selectbox("Patient", patient_names, 
                                              patient_names.index(appointment['patientName'])) if patient_names else st.info("No patients")
                    doctor_name = st.selectbox("Doctor", doctor_names, 
                                             doctor_names.index(appointment['doctorName'])) if doctor_names else st.info("No doctors")
                    
                    col1, col2 = st.columns(2)
                    update = col1.form_submit_button("Update")
                    delete = col2.form_submit_button("Delete")
                    
                    if update:
                        data = {
                            "patientName": patient_name,
                            "doctorName": doctor_name,
                            "appointmentDateTime": get_current_datetime()
                        }
                        db.update_appointment(selected_aid, data)
                        st.success("Updated")
                        st.rerun()
                    elif delete:
                        db.delete_appointment(selected_aid)
                        st.success("Deleted")
                        st.rerun()
    
    with tab2:
        appointments = db.get_all_appointments()
        if appointments:
            df = pd.DataFrame(appointments)
            st.dataframe(df)

def reset_data():
    st.header("Reset Data")
    st.warning("This will delete all data permanently")
    
    if st.button("Reset All Data", type="primary"):
        db.reset_all_data()
        st.success("Data reset complete")
        st.rerun()

if __name__ == "__main__":
    main()