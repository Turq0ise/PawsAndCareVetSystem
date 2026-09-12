class owner:
    def __init__(self, owner_id, name, contact):
        self.name = name
        self.owner_id = owner_id
        self.contact = contact

class ClinicDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClinicDatabase, cls).__new__(cls)
            cls._instance.owners = []
        return cls._instance

    def add_owner(self, owner):
        self.owners.append(owner)

    def view_owners(self):
        for owner in self.owners:
            print(f"Owner ID: {owner.owner_id}, Name: {owner.name}, Contact: {owner.contact}")

def pet_owner_management():
    while True:
        print("\nPet Owner Management Menu:")
        print("1. Add Owner")
        print("2. View Owners")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            owner_id = input("Enter Owner ID: ")
            name = input("Enter Owner Name: ")
            contact = input("Enter Owner Contact: ")
            new_owner = owner(owner_id, name, contact)
            ClinicDatabase().add_owner(new_owner)
            print("Owner added successfully.")
        elif choice == '2':
            ClinicDatabase().view_owners()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

pet_owner_management()

    

