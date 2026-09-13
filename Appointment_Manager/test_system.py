import unittest
from database import ClinicDatabase
from models import Owner, PetFactory
from services.AppointmentManagement import AppointmentManager

class TestAppointmentSystem(unittest.TestCase):
    def setUp(self):
        self.db = ClinicDatabase()
        self.db.clear_database()
        
        self.db.owners["O01"] = Owner("O01", "Alice Smith", "555-0192")
        self.db.pets["P01"] = PetFactory.create_pet("P01", "Buddy", "Dog", "O01")
        self.manager = AppointmentManager()

    def test_singleton_instance(self):
        db1 = ClinicDatabase()
        db2 = ClinicDatabase()
        self.assertIs(db1, db2, "ClinicDatabase is not a true Singleton!")

    def test_schedule_appointment(self):
        appt = self.manager.schedule_appointment("A01", "P01", "2026-06-10 10:00 AM")
        self.assertEqual(appt.status, "Scheduled")
        self.assertIn("A01", self.db.appointments)

    def test_cancel_appointment(self):
        self.manager.schedule_appointment("A01", "P01", "2026-06-10 10:00 AM")
        self.manager.cancel_appointment("A01")
        self.assertEqual(self.db.appointments["A01"].status, "Cancelled")

if __name__ == "__main__":
    unittest.main()