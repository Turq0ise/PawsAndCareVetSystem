from abc import ABC, abstractmethod
from modules.idGen import idGen

class Owner:
    def __init__(self, owner_id, name, contact_number):
        self.owner_id = owner_id or idGen(contact_number, "OWNER")
        self.name = name
        self.contact_number = contact_number

    def to_dict(self):
        return {
            "owner_id": self.owner_id,
            "name": self.name,
            "contact_number": self.contact_number,
        }

class Pet(ABC):
    def __init__(self, name, owner_id, pet_id, age):
        self.pet_id = pet_id or idGen(f"{owner_id}_{name}", "PET")
        self.name = name
        self.owner_id = owner_id
        self.age = age

    @property
    @abstractmethod
    def species(self) -> str:
        """Returns the species name matching the database CHECK constraint."""
        pass

    def to_dict(self):
        return {
            "pet_id": self.pet_id,
            "owner_id": self.owner_id,
            "name": self.name,
            "species": self.species,
            "age": self.age,
        }

class Dog(Pet):
    @property
    def species(self) -> str:
        return "Dog"


class Cat(Pet):
    @property
    def species(self) -> str:
        return "Cat"


class Bird(Pet):
    @property
    def species(self) -> str:
        return "Bird"


class Rabbit(Pet):
    @property
    def species(self) -> str:
        return "Rabbit"

class PetFactory:
    valid_species = {
        "dog": Dog,
        "cat": Cat,
        "bird": Bird,
        "rabbit": Rabbit,
    }

    @classmethod
    def create_pet(cls, species, name, owner_id, pet_id, age):
        normalized_species = species.strip().lower()

        pet_class = cls.valid_species.get(normalized_species)
        if not pet_class:
            valid_types = ", ".join([s.capitalize() for s in cls.valid_species.keys()])
            raise ValueError(
                f"Unsupported species '{species}'. Supported types: {valid_types}"
            )

        return pet_class(name=name, owner_id=owner_id, pet_id=pet_id, age=age)

class Appointment:
    valid_status = {"Scheduled", "Completed", "Cancelled"}

    def __init__(
        self,
        pet_id: str,
        date: str,
        time: str,
        reason: str = "",
        status: str = "Scheduled",
        appointment_id: str = None,
    ):
        if status not in self.valid_status:
            raise ValueError(
                f"Invalid status '{status}'. Must be one of: {self.valid_status}"
            )

        self.appointment_id = appointment_id or idGen(f"{pet_id}_{date}_{time}", "APPOINTMENT")
        self.pet_id = pet_id
        self.date = date
        self.time = time
        self.reason = reason
        self.status = status

    def to_dict(self):
        return {
            "appointment_id": self.appointment_id,
            "pet_id": self.pet_id,
            "reason": self.reason,
            "date": self.date,
            "time": self.time,
            "status": self.status,
        }