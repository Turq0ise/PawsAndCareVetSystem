import unittest
from database import ClinicDatabase

class TestSingletonInstance(unittest.TestCase):

    def setUp(self):
        ClinicDatabase.reset_instance()

    def tearDown(self):
        ClinicDatabase.reset_instance()

    def test_singleton_returns_identical_instance(self):
        db1 = ClinicDatabase(":memory:")
        db2 = ClinicDatabase(":memory:")
        self.assertIs(db1, db2)

    def test_reset_creates_new_instance(self):
        db1 = ClinicDatabase(":memory:")
        ClinicDatabase.reset_instance()
        db2 = ClinicDatabase(":memory:")
        self.assertIsNot(db1, db2)

if __name__ == "__main__":
    unittest.main()