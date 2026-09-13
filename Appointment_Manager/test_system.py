"""Integration tests for the current SQLite-backed service API.

Run from the project root:
python -m unittest discover -s Appointment_Manager -p 'test_*.py' -v
"""
import unittest
from database import ClinicDatabase
from services import OwnerManagement, PetManagement, AppointmentManagement

class TestAppointmentSystem(unittest.TestCase):
    def setUp(self):
        ClinicDatabase.reset_instance()
        self.db = ClinicDatabase(':memory:')
        owner = OwnerManagement(self.db).register_owner('Alice Smith', '09123456789')
        self.pet = PetManagement(self.db).add_pet(owner.owner_id, 'Dog', 'Buddy')
        self.manager = AppointmentManagement(self.db)

    def tearDown(self):
        ClinicDatabase.reset_instance()

    def test_singleton_instance(self):
        self.assertIs(self.db, ClinicDatabase())

    def test_schedule_appointment(self):
        appt = self.manager.schedule_appointment(self.pet.pet_id, '2026-10-20', '10:00')
        self.assertEqual(appt.status, 'Scheduled')
        self.assertIsNotNone(self.manager.get_appointment_by_id(appt.appointment_id))

    def test_cancel_appointment(self):
        appt = self.manager.schedule_appointment(self.pet.pet_id, '2026-10-20', '10:00')
        self.manager.cancel_appointment(appt.appointment_id)
        self.assertEqual(self.manager.get_appointment_by_id(appt.appointment_id).status, 'Cancelled')

if __name__ == '__main__':
    unittest.main()
