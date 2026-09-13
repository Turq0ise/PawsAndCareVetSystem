import unittest
from database import ClinicDatabase
from models import Dog, Cat, Bird, Rabbit
from services.OwnerManagement import OwnerManagement
from services.PetManagement import PetManagement

class TestPetRecord(unittest.TestCase):

    def setUp(self):
        ClinicDatabase.reset_instance()
        self.db = ClinicDatabase(":memory:")
        self.owner_management = OwnerManagement(self.db)
        self.pet_management = PetManagement(self.db)
        self.owner = self.owner_management.register_owner("Juan Dela Cruz", "09181234567")

    def tearDown(self):
        ClinicDatabase.reset_instance()

    def test_add_dog_pet_record_factory_instantiation(self):
        pet = self.pet_management.add_pet(self.owner.owner_id, "Dog", "Bantay")
        self.assertIsInstance(pet, Dog)
        self.assertEqual(pet.species, "Dog")
        self.assertEqual(pet.owner_id, self.owner.owner_id)

    def test_add_supported_pet_subclasses(self):
        cat = self.pet_management.add_pet(self.owner.owner_id, "Cat", "Munimuni")
        bird = self.pet_management.add_pet(self.owner.owner_id, "Bird", "Tweety")
        rabbit = self.pet_management.add_pet(self.owner.owner_id, "Rabbit", "Bugs")

        self.assertIsInstance(cat, Cat)
        self.assertIsInstance(bird, Bird)
        self.assertIsInstance(rabbit, Rabbit)

    def test_add_pet_unsupported_species_fails(self):
        with self.assertRaises(ValueError):
            self.pet_management.add_pet(self.owner.owner_id, "Hamster", "Pip")

    def test_add_pet_nonexistent_owner_fails(self):
        with self.assertRaises(ValueError):
            self.pet_management.add_pet("non-existent-owner-id", "Dog", "Sparky")

if __name__ == "__main__":
    unittest.main()