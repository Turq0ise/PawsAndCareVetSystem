import unittest
from database import ClinicDatabase
from services.OwnerManagement import OwnerManagement
from services.PetManagement import PetManagement
from services.AppointmentManagement import AppointmentManagement

class TestCancelAppointment(unittest.TestCase):

    def setUp(self):
        ClinicDatabase.reset_instance()
        self.db = ClinicDatabase(":memory:")
        self.owner_management = OwnerManagement(self.db)
        self.pet_management = PetManagement(self.db)
        self.appointment_management = AppointmentManagement(self.db)

        self.owner = self.owner_management.register_owner("Ana Reyes", "09201234567")
        self.pet = self.pet_management.add_pet(self.owner.owner_id, "Dog", "Baron", 4)
        self.appointment = self.appointment_management.schedule_appointment(
            pet_id=self.pet.pet_id,
            date="2026-10-20",
            time="02:00 PM",
            reason="Grooming"
        )

    def tearDown(self):
        ClinicDatabase.reset_instance()

    def test_cancel_appointment_success(self):
        result = self.appointment_management.cancel_appointment(self.appointment.appointment_id)
        self.assertTrue(result)

        updated = self.appointment_management.get_appointment_by_id(self.appointment.appointment_id)
        self.assertEqual(updated.status, "Cancelled")

    def test_cancel_already_cancelled_appointment_fails(self):
        self.appointment_management.cancel_appointment(self.appointment.appointment_id)
        with self.assertRaises(ValueError):
            self.appointment_management.cancel_appointment(self.appointment.appointment_id)

    def test_cancel_nonexistent_appointment_returns_false(self):
        result = self.appointment_management.cancel_appointment("invalid-appointment-id")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()