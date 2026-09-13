from database import ClinicDatabase
from models import Appointment

class AppointmentManager:
    def __init__(self):
        self.db = ClinicDatabase()

    def schedule_appointment(self, appointment_id, pet_id, date_time):
        if pet_id not in self.db.pets:
            raise ValueError("Pet ID does not exist in the database.")
        if appointment_id in self.db.appointments:
            raise ValueError("Appointment ID already exists.")
        
        appt = Appointment(appointment_id, pet_id, date_time)
        self.db.appointments[appointment_id] = appt
        return appt

    def cancel_appointment(self, appointment_id):
        if appointment_id not in self.db.appointments:
            raise ValueError("Appointment ID not found.")
        self.db.appointments[appointment_id].status = "Cancelled"

    def update_status(self, appointment_id, status):
        valid_statuses = ["Scheduled", "Completed", "Cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        if appointment_id not in self.db.appointments:
            raise ValueError("Appointment ID not found.")
        self.db.appointments[appointment_id].status = status

    def view_appointments(self):
        return self.db.appointments