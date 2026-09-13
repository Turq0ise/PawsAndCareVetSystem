import sqlite3
from database import ClinicDatabase
from models import Pet, PetFactory

class PetManagement:
    """Service layer handling business logic for Pets."""

    def __init__(self, db):
        self.db = db or ClinicDatabase()

    def add_pet(self, owner_id, pet_type, name, age=None):
        """Creates a pet via PetFactory and links it to an existing owner.

        Args:
            owner_id: The UUID of the pet's owner.
            pet_type: The species (Dog, Cat, Bird, Rabbit).
            name: The pet's name.

        Returns:
            Pet: The concrete Pet subclass instance (Dog, Cat, etc.).

        Raises:
            ValueError: If validation fails, species is invalid, or owner does not exist.
        """
        clean_name = name.strip()
        clean_owner_id = owner_id.strip()

        if not clean_name:
            raise ValueError("Pet name cannot be empty.")
        if not clean_owner_id:
            raise ValueError("Owner ID cannot be empty.")

        owner_exists = self.db.fetch_one(
            "SELECT owner_id FROM owners WHERE owner_id = ?", (clean_owner_id,)
        )
        if not owner_exists:
            raise ValueError(f"Owner with ID '{clean_owner_id}' does not exist.")

        pet = PetFactory.create_pet(
            species=pet_type,
            name=clean_name,
            owner_id=clean_owner_id,
            pet_id=None,
            age=age,
        )

        query = """
            INSERT INTO pets (pet_id, owner_id, name, species, age)
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            self.db.execute_query(
                query, (pet.pet_id, pet.owner_id, pet.name, pet.species, pet.age)
            )
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Failed to add pet: {e}")

        return pet

    def get_pet_by_id(self, pet_id):
        """Retrieves a single pet by its UUID and reconstructs it via PetFactory."""
        query = "SELECT pet_id, owner_id, name, species, age FROM pets WHERE pet_id = ?"
        row = self.db.fetch_one(query, (pet_id,))

        if not row:
            return None

        return PetFactory.create_pet(
            species=row["species"],
            name=row["name"],
            owner_id=row["owner_id"],
            age=row["age"],
            pet_id=row["pet_id"],
        )

    def get_pets_by_owner(self, owner_id):
        """Retrieves all pets belonging to a specific owner."""
        query = "SELECT pet_id, owner_id, name, species, age FROM pets WHERE owner_id = ?"
        rows = self.db.fetch_all(query, (owner_id,))

        return [
            PetFactory.create_pet(
                species=row["species"],
                name=row["name"],
                owner_id=row["owner_id"],
                age=row["age"],
                pet_id=row["pet_id"],
            )
            for row in rows
        ]

    def get_all_pets(self):
        """Retrieves all pets registered in the clinic."""
        query = "SELECT pet_id, owner_id, name, species, age FROM pets ORDER BY name ASC"
        rows = self.db.fetch_all(query)

        return [
            PetFactory.create_pet(
                species=row["species"],
                name=row["name"],
                owner_id=row["owner_id"],
                age=row["age"],
                pet_id=row["pet_id"],
            )
            for row in rows
        ]
