import unittest
from database import ClinicDatabase
from services.OwnerManagement import OwnerManagement

class TestOwnerRegistration(unittest.TestCase):

    def setUp(self):
        ClinicDatabase.reset_instance()
        self.db = ClinicDatabase(":memory:")
        self.owner_management = OwnerManagement(self.db)

    def tearDown(self):
        ClinicDatabase.reset_instance()

    def test_register_pet_owner_success(self):
        owner = self.owner_management.register_owner("Maria Santos", "09171234567")
        
        self.assertIsNotNone(owner.owner_id)
        self.assertEqual(owner.name, "Maria Santos")
        self.assertEqual(owner.contact_number, "09171234567")

        fetched = self.owner_management.get_owner_by_id(owner.owner_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "Maria Santos")

    def test_register_owner_duplicate_contact_fails(self):
        self.owner_management.register_owner("Maria Santos", "09171234567")
        with self.assertRaises(ValueError):
            self.owner_management.register_owner("Maria Clone", "09171234567")

    def test_register_owner_empty_fields_fail(self):
        with self.assertRaises(ValueError):
            self.owner_management.register_owner("", "09171234567")
        with self.assertRaises(ValueError):
            self.owner_management.register_owner("Valid Name", "")

if __name__ == "__main__":
    unittest.main()