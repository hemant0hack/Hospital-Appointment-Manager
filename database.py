# database.py
import sqlite3
from datetime import datetime

class HospitalDatabase:
    def __init__(self, db_name="hospital.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                address TEXT,
                disease TEXT NOT NULL,
                referred_by TEXT,
                admission_datetime TEXT NOT NULL
            )
        ''')
        
        # Create doctors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                experience INTEGER NOT NULL
            )
        ''')
        
        # Create appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id TEXT PRIMARY KEY,
                patient_name TEXT NOT NULL,
                doctor_name TEXT NOT NULL,
                appointment_datetime TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Patient methods
    def add_patient(self, patient_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patients (id, name, age, gender, address, disease, referred_by, admission_datetime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            patient_data['id'],
            patient_data['name'],
            patient_data['age'],
            patient_data['gender'],
            patient_data['address'],
            patient_data['disease'],
            patient_data['REFERRED_BY'],
            patient_data['admissionDateTime']
        ))
        conn.commit()
        conn.close()
    
    def get_all_patients(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patients')
        patients = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0],
            'name': row[1],
            'age': row[2],
            'gender': row[3],
            'address': row[4],
            'disease': row[5],
            'REFERRED_BY': row[6],
            'admissionDateTime': row[7]
        } for row in patients]
    
    def get_patient_by_id(self, patient_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'address': row[4],
                'disease': row[5],
                'REFERRED_BY': row[6],
                'admissionDateTime': row[7]
            }
        return None
    
    def update_patient(self, patient_id, updated_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE patients 
            SET name = ?, age = ?, gender = ?, address = ?, disease = ?, referred_by = ?, admission_datetime = ?
            WHERE id = ?
        ''', (
            updated_data['name'],
            updated_data['age'],
            updated_data['gender'],
            updated_data['address'],
            updated_data['disease'],
            updated_data['REFERRED_BY'],
            updated_data['admissionDateTime'],
            patient_id
        ))
        conn.commit()
        conn.close()
    
    def delete_patient(self, patient_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        conn.commit()
        conn.close()
    
    # Doctor methods
    def add_doctor(self, doctor_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO doctors (id, name, specialization, experience)
            VALUES (?, ?, ?, ?)
        ''', (
            doctor_data['id'],
            doctor_data['name'],
            doctor_data['specialization'],
            doctor_data['experience']
        ))
        conn.commit()
        conn.close()
    
    def get_all_doctors(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM doctors')
        doctors = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0],
            'name': row[1],
            'specialization': row[2],
            'experience': row[3]
        } for row in doctors]
    
    def get_doctor_by_id(self, doctor_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM doctors WHERE id = ?', (doctor_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'specialization': row[2],
                'experience': row[3]
            }
        return None
    
    def update_doctor(self, doctor_id, updated_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE doctors 
            SET name = ?, specialization = ?, experience = ?
            WHERE id = ?
        ''', (
            updated_data['name'],
            updated_data['specialization'],
            updated_data['experience'],
            doctor_id
        ))
        conn.commit()
        conn.close()
    
    def delete_doctor(self, doctor_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM doctors WHERE id = ?', (doctor_id,))
        conn.commit()
        conn.close()
    
    # Appointment methods
    def add_appointment(self, appointment_data):
        # Check for overlapping appointments
        if self.has_overlapping_appointments(
            appointment_data['doctorName'],
            appointment_data['appointmentDateTime']
        ):
            return False, "This time slot is already booked for the selected doctor"
            
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO appointments (id, patient_name, doctor_name, appointment_datetime)
            VALUES (?, ?, ?, ?)
        ''', (
            appointment_data['id'],
            appointment_data['patientName'],
            appointment_data['doctorName'],
            appointment_data['appointmentDateTime']
        ))
        conn.commit()
        conn.close()
        return True, "Appointment scheduled successfully"
    
    def has_overlapping_appointments(self, doctor_name, new_appointment_time):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Convert string to datetime for comparison
        new_time = datetime.strptime(new_appointment_time, "%d-%m-%Y %H:%M:%S")
        
        # Get all appointments for the doctor on the same day
        day_start = new_time.replace(hour=0, minute=0, second=0).strftime("%d-%m-%Y %H:%M:%S")
        day_end = new_time.replace(hour=23, minute=59, second=59).strftime("%d-%m-%Y %H:%M:%S")
        
        cursor.execute('''
            SELECT appointment_datetime 
            FROM appointments 
            WHERE doctor_name = ? 
            AND appointment_datetime BETWEEN ? AND ?
        ''', (doctor_name, day_start, day_end))
        
        existing_appointments = cursor.fetchall()
        conn.close()
        
        # Check for 30-minute slot conflicts
        for (existing_time,) in existing_appointments:
            existing_dt = datetime.strptime(existing_time, "%d-%m-%Y %H:%M:%S")
            time_difference = abs((new_time - existing_dt).total_seconds() / 60)
            if time_difference < 30:  # Less than 30 minutes apart
                return True
        
        return False
    
    def get_all_appointments(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM appointments 
            ORDER BY appointment_datetime ASC
        ''')
        appointments = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0],
            'patientName': row[1],
            'doctorName': row[2],
            'appointmentDateTime': row[3]
        } for row in appointments]
    
    def get_appointment_by_id(self, appointment_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM appointments WHERE id = ?', (appointment_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'patientName': row[1],
                'doctorName': row[2],
                'appointmentDateTime': row[3]
            }
        return None
        
    def get_doctor_schedule(self, doctor_name, date):
        """Get all appointments for a doctor on a specific date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Convert date to datetime range for the whole day
        day_start = f"{date} 00:00:00"
        day_end = f"{date} 23:59:59"
        
        cursor.execute('''
            SELECT appointment_datetime, patient_name 
            FROM appointments 
            WHERE doctor_name = ? 
            AND appointment_datetime BETWEEN ? AND ?
            ORDER BY appointment_datetime ASC
        ''', (doctor_name, day_start, day_end))
        
        schedule = cursor.fetchall()
        conn.close()
        
        return [{
            'time': datetime.strptime(row[0], "%d-%m-%Y %H:%M:%S").strftime("%H:%M"),
            'patient': row[1]
        } for row in schedule]
    
    def update_appointment(self, appointment_id, updated_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE appointments 
            SET patient_name = ?, doctor_name = ?, appointment_datetime = ?
            WHERE id = ?
        ''', (
            updated_data['patientName'],
            updated_data['doctorName'],
            updated_data['appointmentDateTime'],
            appointment_id
        ))
        conn.commit()
        conn.close()
    
    def delete_appointment(self, appointment_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
        conn.commit()
        conn.close()
    
    # Reset all data
    def reset_all_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM patients')
        cursor.execute('DELETE FROM doctors')
        cursor.execute('DELETE FROM appointments')
        conn.commit()
        conn.close()