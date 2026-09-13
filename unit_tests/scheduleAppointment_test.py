import unittest
from database import ClinicDatabase
from services.OwnerManagement import OwnerManagement
from services.PetManagement import PetManagement
from services.AppointmentManagement import AppointmentManagement

class TestScheduleAppointment(unittest.TestCase):

    def setUp(self):
        ClinicDatabase.reset_instance()
        self.db = ClinicDatabase(":memory:")
        self.owner_management = OwnerManagement(self.db)
        self.pet_management = PetManagement(self.db)
        self.appointment_management = AppointmentManagement(self.db)

        self.owner = self.owner_management.register_owner("Pedro Penduko", "09191234567")
        self.pet = self.pet_management.add_pet(self.owner.owner_id, "Cat", "Ming", 2)

    def tearDown(self):
        ClinicDatabase.reset_instance()

    def test_schedule_appointment_success(self):
        appointment = self.appointment_management.schedule_appointment(
            pet_id=self.pet.pet_id,
            date="2026-10-15",
            time="10:00 AM",
            reason="Rabies Vaccine"
        )
        self.assertIsNotNone(appointment.appointment_id)
        self.assertEqual(appointment.status, "Scheduled")

        retrieved = self.appointment_management.get_appointment_by_id(appointment.appointment_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.status, "Scheduled")

    def test_schedule_appointment_nonexistent_pet_fails(self):
        with self.assertRaises(ValueError):
            self.appointment_management.schedule_appointment(
                pet_id="fake-pet-id",
                date="2026-10-15",
                time="10:00 AM",
                reason="Checkup"
            )

    def test_schedule_appointment_duplicate_slot_fails(self):
        self.appointment_management.schedule_appointment(
            pet_id=self.pet.pet_id,
            date="2026-10-15",
            time="10:00 AM",
            reason="Initial Exam"
        )
        with self.assertRaises(ValueError):
            self.appointment_management.schedule_appointment(
                pet_id=self.pet.pet_id,
                date="2026-10-15",
                time="10:00 AM",
                reason="Second Attempt"
            )

if __name__ == "__main__":
    unittest.main()