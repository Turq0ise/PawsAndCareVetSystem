class pet:
    def __init__(self, pet_name, species, age, owner_id):
        self.pet_id = pet_name
        self.species = species
        self.age = age
        self.owner_id = owner_id

    def display_info(self):
        print("Pet Name: " + str(self.pet_id))
        print("Species: " + self.species)
        print("Age: " + str(self.age))
        print("Owner ID: " + str(self.owner_id))

    def get_info(self):
        return f"{self.pet_id} is a {self.age}-year-old {self.species}."
    
class dog(pet):
    pass

class cat(pet):
    pass    

class bird(pet):
    pass    

class rabbit(pet):
    pass    

class PetManagement:
    
    def __init__(self):
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)
        print("Pet record added successfully.")

    def view_pets(self):
        if not self.pets:
            print("No pet records found.")
            return
        for pet in self.pets:
            pet.display_info()
            print("--------------------")

    def view_owner_pets(self, owner_id):
        for pet in self.pets:
            if pet.owner_id == owner_id:
                pet.display_info()
                print("--------------------")
                found = True

            else:
                found = False

        if not found:
            print("No pets found for the given owner ID.")

pet_management = PetManagement()



