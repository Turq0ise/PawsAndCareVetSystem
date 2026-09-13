import sqlite3
from database import ClinicDatabase
from models import Appointment

class AppointmentManagement:
    """Service layer handling booking, cancellation, and appointment schedules."""

    def __init__(self, db):
        self.db = db or ClinicDatabase()

    def schedule_appointment(
        self, pet_id: str, date: str, time: str, reason: str = ""
    ) -> Appointment:
        """Schedules a new appointment for a pet.

        Args:
            pet_id: UUID of the pet.
            date: Appointment date (e.g., 'YYYY-MM-DD').
            time: Appointment time (e.g., '14:30' or '02:30 PM').
            reason: Purpose of the clinic visit.

        Returns:
            Appointment: The newly created Appointment instance.

        Raises:
            ValueError: If input validation fails, pet doesn't exist, or slot conflicts.
        """
        clean_pet_id = pet_id.strip()
        clean_date = date.strip()
        clean_time = time.strip()
        clean_reason = reason.strip()

        if not clean_pet_id:
            raise ValueError("Pet ID cannot be empty.")
        if not clean_date or not clean_time:
            raise ValueError("Date and time must both be provided.")

        pet_exists = self.db.fetch_one(
            "SELECT pet_id FROM pets WHERE pet_id = ?", (clean_pet_id,)
        )
        if not pet_exists:
            raise ValueError(f"Pet with ID '{clean_pet_id}' does not exist.")

        appointment = Appointment(
            pet_id=clean_pet_id,
            date=clean_date,
            time=clean_time,
            reason=clean_reason,
            status="Scheduled",
        )

        query = """
            INSERT INTO appointments (appointment_id, pet_id, reason, date, time, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            self.db.execute_query(
                query,
                (
                    appointment.appointment_id,
                    appointment.pet_id,
                    appointment.reason,
                    appointment.date,
                    appointment.time,
                    appointment.status,
                ),
            )
        except sqlite3.IntegrityError:
            raise ValueError(
                f"An appointment for this pet at {clean_date} {clean_time} already exists."
            )

        return appointment

    def cancel_appointment(self, appointment_id):
        """Cancels an existing appointment by setting its status to 'Cancelled'.

        Args:
            appointment_id: The UUID of the appointment to cancel.

        Returns:
            bool: True if the appointment was cancelled, False if it was not found.

        Raises:
            ValueError: If the appointment is already cancelled or completed.
        """
        record = self.get_appointment_by_id(appointment_id)
        if not record:
            return False

        if record.status == "Cancelled":
            raise ValueError(f"Appointment '{appointment_id}' is already cancelled.")
        if record.status == "Completed":
            raise ValueError(f"Cannot cancel a completed appointment.")

        query = "UPDATE appointments SET status = 'Cancelled' WHERE appointment_id = ?"
        self.db.execute_query(query, (appointment_id,))
        return True

    def update_status(self, appointment_id, new_status):
        """Updates the status of an appointment ('Scheduled', 'Completed', 'Cancelled')."""
        if new_status not in Appointment.valid_status:
            raise ValueError(
                f"Invalid status '{new_status}'. Allowed: {Appointment.valid_status}"
            )

        record = self.get_appointment_by_id(appointment_id)
        if not record:
            return False

        query = "UPDATE appointments SET status = ? WHERE appointment_id = ?"
        self.db.execute_query(query, (new_status, appointment_id))
        return True

    def get_appointment_by_id(self, appointment_id):
        """Retrieves a single appointment by its UUID."""
        query = """
            SELECT appointment_id, pet_id, reason, date, time, status
            FROM appointments
            WHERE appointment_id = ?
        """
        row = self.db.fetch_one(query, (appointment_id,))
        if not row:
            return None

        return Appointment(
            appointment_id=row["appointment_id"],
            pet_id=row["pet_id"],
            reason=row["reason"],
            date=row["date"],
            time=row["time"],
            status=row["status"],
        )

    def get_appointments(self, status=None):
        """Retrieves appointments, optionally filtered by status."""
        if status:
            if status not in Appointment.valid_status:
                raise ValueError(f"Invalid status filter '{status}'.")
            query = """
                SELECT appointment_id, pet_id, reason, date, time, status
                FROM appointments
                WHERE status = ?
                ORDER BY date ASC, time ASC
            """
            rows = self.db.fetch_all(query, (status,))
        else:
            query = """
                SELECT appointment_id, pet_id, reason, date, time, status
                FROM appointments
                ORDER BY date ASC, time ASC
            """
            rows = self.db.fetch_all(query)

        return [
            Appointment(
                appointment_id=row["appointment_id"],
                pet_id=row["pet_id"],
                reason=row["reason"],
                date=row["date"],
                time=row["time"],
                status=row["status"],
            )
            for row in rows
        ]
