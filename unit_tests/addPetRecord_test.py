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
        self.owner = self.owner_management.register_owner("Efren", "09171234567")

    def tearDown(self):
        ClinicDatabase.reset_instance()

    def test_add_dog_pet_record_factory_instantiation(self):
        pet = self.pet_management.add_pet(self.owner.owner_id, "Dog", "Mapuworf", age=3)
        self.assertIsInstance(pet, Dog)
        self.assertEqual(pet.species, "Dog")
        self.assertEqual(pet.owner_id, self.owner.owner_id)
        self.assertEqual(pet.age, 3)

        retrieved = self.pet_management.get_pet_by_id(pet.pet_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.age, 3)

    def test_add_pet_without_age_defaults_to_none(self):
        pet = self.pet_management.add_pet(self.owner.owner_id, "Cat", "Catgpt", age=None)
        self.assertIsNone(pet.age)

        retrieved = self.pet_management.get_pet_by_id(pet.pet_id)
        self.assertIsNotNone(retrieved)
        self.assertIsNone(retrieved.age)

    def test_add_pet_negative_age_fails(self):
        with self.assertRaises(ValueError):
            self.pet_management.add_pet(
                self.owner.owner_id, "Cat", "Catgpt", age=-1
            )

    def test_add_supported_pet_subclasses(self):
        cat = self.pet_management.add_pet(self.owner.owner_id, "Cat", "Catgpt", age=2)
        bird = self.pet_management.add_pet(self.owner.owner_id, "Bird", "Reebz", age=1)
        rabbit = self.pet_management.add_pet(self.owner.owner_id, "Rabbit", "Bugs", age=4)

        self.assertIsInstance(cat, Cat)
        self.assertIsInstance(bird, Bird)
        self.assertIsInstance(rabbit, Rabbit)
        self.assertEqual(cat.age, 2)
        self.assertEqual(bird.age, 1)
        self.assertEqual(rabbit.age, 4)

    def test_add_pet_unsupported_species_fails(self):
        with self.assertRaises(ValueError):
            self.pet_management.add_pet(self.owner.owner_id, "Hamster", "Pip", age=1)

    def test_add_pet_nonexistent_owner_fails(self):
        with self.assertRaises(ValueError):
            self.pet_management.add_pet("non-existent-owner-id", "Dog", "Sparky", age=1)

if __name__ == "__main__":
    unittest.main()