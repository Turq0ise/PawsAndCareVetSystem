class Owner:
    def __init__(self, owner_id,name, contact_number):
        self.owner_id = owner_id
        self.name = name
        self.contact_number = contact_number

class Pet:
    def __init__(self,pet_id,name,species,owner_id):
        self.pet_id = pet_id
        self.name = name
        self.species = species
        self.owner_id = owner_id

class Appointment:
    def __init__(self,appointment_id,pet_id,date,time, status= "Scheduled"):
        self.appointment_id= appointment_id
        self.pet_id= pet_id
        self.date = date
        self.time = time

class PetFactory:
    @staticmethod
    def create_pet(pet_id,name,species,owner_id):
        valid_species= ["Dog", "Cat", "Bird","Rabbit"]
        if species not in valid_species:
            raise ValueError(f"Invalid species. Must be one of {valid_species}")
        return Pet(pet_id,name,species,owner_id)