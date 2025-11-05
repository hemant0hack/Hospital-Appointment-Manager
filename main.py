#!/usr/bin/env python3
from datetime import datetime
import sys

patients = []  # list of dicts
doctors = []
appointments = []


def get_current_datetime():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Patients
def add_patient():
    pid = input("Enter Patient ID: ").strip()
    name = input("Enter Patient Name: ").strip()
    try:
        age = int(input("Enter Patient Age: ").strip())
    except ValueError:
        print("Invalid age, setting age to 0")
        age = 0
    gender = input("Enter Patient Gender: ").strip()
    address = input("Enter Patient Address: ").strip()
    disease = input("Enter Patient Disease: ").strip()
    referred_by = input("Enter Referred By: ").strip()
    admission = get_current_datetime()
    patients.append({
        "id": pid,
        "name": name,
        "age": age,
        "gender": gender,
        "address": address,
        "disease": disease,
        "REFERRED_BY": referred_by,
        "admissionDateTime": admission,
    })
    print("Patient added successfully!\n")


def view_patients():
    if not patients:
        print("No patients found.")
        return
    for p in patients:
        print(f"ID: {p['id']} | Name: {p['name']} | Age: {p['age']} | Gender: {p['gender']} | Address: {p['address']} | Disease: {p['disease']} | REFERRED_BY: {p['REFERRED_BY']} | Admission DateTime: {p['admissionDateTime']}")


def find_patient_index_by_id(pid):
    for i, p in enumerate(patients):
        if p['id'] == pid:
            return i
    return -1


def edit_patient():
    pid = input("Enter Patient ID to edit: ").strip()
    idx = find_patient_index_by_id(pid)
    if idx == -1:
        print("Patient not found!")
        return
    p = patients[idx]
    print("What do you want to edit?")
    print("1. Name\n2. Age\n3. Gender\n4. Address\n5. Disease\n6. Referred By")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        p['name'] = input("Enter new Patient Name: ").strip()
    elif choice == '2':
        try:
            p['age'] = int(input("Enter new Patient Age: ").strip())
        except ValueError:
            print("Invalid age, keeping previous value.")
    elif choice == '3':
        p['gender'] = input("Enter new Patient Gender: ").strip()
    elif choice == '4':
        p['address'] = input("Enter new Patient Address: ").strip()
    elif choice == '5':
        p['disease'] = input("Enter new Patient Disease: ").strip()
    elif choice == '6':
        p['REFERRED_BY'] = input("Enter new Referred By: ").strip()
    else:
        print("Invalid choice!")
        return
    p['admissionDateTime'] = get_current_datetime()
    print("Patient record updated successfully!")


def view_patient_by_id():
    pid = input("Enter Patient ID to view: ").strip()
    idx = find_patient_index_by_id(pid)
    if idx == -1:
        print("Patient not found!")
        return
    p = patients[idx]
    print(f"ID: {p['id']} | Name: {p['name']} | Age: {p['age']} | Gender: {p['gender']} | Address: {p['address']} | Disease: {p['disease']} | REFERRED_BY: {p['REFERRED_BY']} | Admission DateTime: {p['admissionDateTime']}")


def delete_patient_by_id():
    pid = input("Enter Patient ID to delete: ").strip()
    idx = find_patient_index_by_id(pid)
    if idx == -1:
        print("Patient not found!")
        return
    patients.pop(idx)
    print("Patient record deleted successfully!")


# Doctors

def add_doctor():
    did = input("Enter Doctor ID: ").strip()
    name = input("Enter Doctor Name: ").strip()
    specialization = input("Enter Doctor Specialization: ").strip()
    try:
        experience = int(input("Enter Doctor Experience (years): ").strip())
    except ValueError:
        print("Invalid experience, setting to 0")
        experience = 0
    doctors.append({
        "id": did,
        "name": name,
        "specialization": specialization,
        "experience": experience,
    })
    print("Doctor added successfully!\n")


def view_doctors():
    if not doctors:
        print("No doctors found.")
        return
    for d in doctors:
        print(f"ID: {d['id']} | Name: {d['name']} | Specialization: {d['specialization']} | Experience: {d['experience']} years")


def find_doctor_index_by_id(did):
    for i, d in enumerate(doctors):
        if d['id'] == did:
            return i
    return -1


def edit_doctor():
    did = input("Enter Doctor ID to edit: ").strip()
    idx = find_doctor_index_by_id(did)
    if idx == -1:
        print("Doctor not found!")
        return
    d = doctors[idx]
    print("What do you want to edit?\n1. Name\n2. Specialization\n3. Experience")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        d['name'] = input("Enter new Doctor Name: ").strip()
    elif choice == '2':
        d['specialization'] = input("Enter new Doctor Specialization: ").strip()
    elif choice == '3':
        try:
            d['experience'] = int(input("Enter new Doctor Experience (years): ").strip())
        except ValueError:
            print("Invalid value, keeping previous experience.")
    else:
        print("Invalid choice!")
        return
    print("Doctor record updated successfully!")


def view_doctor_by_id():
    did = input("Enter Doctor ID to view: ").strip()
    idx = find_doctor_index_by_id(did)
    if idx == -1:
        print("Doctor not found!")
        return
    d = doctors[idx]
    print(f"ID: {d['id']} | Name: {d['name']} | Specialization: {d['specialization']} | Experience: {d['experience']} years")


def delete_doctor_by_id():
    did = input("Enter Doctor ID to delete: ").strip()
    idx = find_doctor_index_by_id(did)
    if idx == -1:
        print("Doctor not found!")
        return
    doctors.pop(idx)
    print("Doctor record deleted successfully!")


# Appointments

def add_appointment():
    aid = input("Enter Appointment ID: ").strip()
    patient_name = input("Enter Patient Name: ").strip()
    doctor_name = input("Enter Doctor Name: ").strip()
    appointment_time = get_current_datetime()
    appointments.append({
        "id": aid,
        "patientName": patient_name,
        "doctorName": doctor_name,
        "appointmentDateTime": appointment_time,
    })
    print("Appointment added successfully!\n")


def view_appointments():
    if not appointments:
        print("No appointments found.")
        return
    for a in appointments:
        print(f"ID: {a['id']} | Patient Name: {a['patientName']} | Doctor Name: {a['doctorName']} | Appointment DateTime: {a['appointmentDateTime']}")


def find_appointment_index_by_id(aid):
    for i, a in enumerate(appointments):
        if a['id'] == aid:
            return i
    return -1


def edit_appointment():
    aid = input("Enter Appointment ID to edit: ").strip()
    idx = find_appointment_index_by_id(aid)
    if idx == -1:
        print("Appointment not found!")
        return
    a = appointments[idx]
    print("What do you want to edit?\n1. Patient Name\n2. Doctor Name")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        a['patientName'] = input("Enter new Patient Name: ").strip()
    elif choice == '2':
        a['doctorName'] = input("Enter new Doctor Name: ").strip()
    else:
        print("Invalid choice!")
        return
    a['appointmentDateTime'] = get_current_datetime()
    print("Appointment record updated successfully!")


def view_appointment_by_id():
    aid = input("Enter Appointment ID to view: ").strip()
    idx = find_appointment_index_by_id(aid)
    if idx == -1:
        print("Appointment not found!")
        return
    a = appointments[idx]
    print(f"ID: {a['id']} | Patient Name: {a['patientName']} | Doctor Name: {a['doctorName']} | Appointment DateTime: {a['appointmentDateTime']}")


def delete_appointment_by_id():
    aid = input("Enter Appointment ID to delete: ").strip()
    idx = find_appointment_index_by_id(aid)
    if idx == -1:
        print("Appointment not found!")
        return
    appointments.pop(idx)
    print("Appointment record deleted successfully!")


def reset_all_data():
    patients.clear()
    doctors.clear()
    appointments.clear()
    print("All data reset successfully!")


# Main loop
def patients_menu():
    print("\n1. Add Patient\n2. View Patients\n3. Edit Patient\n4. View Patient by ID\n5. Delete Patient by ID\n6. Back to Main Menu")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        add_patient()
    elif choice == '2':
        view_patients()
    elif choice == '3':
        edit_patient()
    elif choice == '4':
        view_patient_by_id()
    elif choice == '5':
        delete_patient_by_id()
    elif choice == '6':
        return
    else:
        print("Invalid choice!")


def doctors_menu():
    print("\n1. Add Doctor\n2. View Doctors\n3. Edit Doctor\n4. View Doctor by ID\n5. Delete Doctor by ID\n6. Back to Main Menu")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        add_doctor()
    elif choice == '2':
        view_doctors()
    elif choice == '3':
        edit_doctor()
    elif choice == '4':
        view_doctor_by_id()
    elif choice == '5':
        delete_doctor_by_id()
    elif choice == '6':
        return
    else:
        print("Invalid choice!")


def appointments_menu():
    print("\n1. Add Appointment\n2. View Appointments\n3. Edit Appointment\n4. View Appointment by ID\n5. Delete Appointment by ID\n6. Back to Main Menu")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        add_appointment()
    elif choice == '2':
        view_appointments()
    elif choice == '3':
        edit_appointment()
    elif choice == '4':
        view_appointment_by_id()
    elif choice == '5':
        delete_appointment_by_id()
    elif choice == '6':
        return
    else:
        print("Invalid choice!")


def main():
    while True:
        print("\n1. Patients\n2. Doctors\n3. Appointments\n4. Reset All Data\n5. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            patients_menu()
        elif choice == '2':
            doctors_menu()
        elif choice == '3':
            appointments_menu()
        elif choice == '4':
            reset_all_data()
        elif choice == '5':
            print("----------------Thank You----------------")
            sys.exit(0)
        else:
            print("Invalid choice!")


if __name__ == '__main__':
    main()
