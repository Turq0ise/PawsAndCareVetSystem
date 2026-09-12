class Owner:
    def __init__(self, owner_id,name, contact_number):
        self.owner_id = owner_id
        self.name = name
        self.contact_number = contact_number

class Pet:
    def __init__(self,pet_id,owner_id,name,species,age):
        self.pet_id = pet_id
        self.owner_id = owner_id
        self.name = name
        self.species = species
        self.age = age

class Appointment:
    def __init__(self,appointment_id,pet_id,reason,date,time, status):
        self.appointment_id= appointment_id
        self.pet_id= pet_id
        self.reason = reason
        self.date = date
        self.time = time
        self.status = status

class PetFactory:
    @staticmethod
    def create_pet(pet_id,name,species,owner_id):
        valid_species= ["Dog", "Cat", "Bird","Rabbit"]
        if species not in valid_species:
            raise ValueError(f"Invalid species. Must be one of {valid_species}")
        return Pet(pet_id,name,species,owner_id)