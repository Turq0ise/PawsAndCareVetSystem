import sys
from database import ClinicDatabase
from services import AppointmentManagement, OwnerManagement, PetManagement

def print_header(title: str):
    print("\n" + "=" * 50)
    print(f" {title.upper()}")
    print("=" * 50)

def register_owner_flow(owner_service: OwnerManagement):
    print_header("Register Pet Owner")
    name = input("Enter Owner Full Name: ").strip()
    contact = input("Enter Contact Number: ").strip()

    try:
        owner = owner_service.register_owner(name, contact)
        print(f"\n[SUCCESS] Owner registered successfully!")
        print(f"Owner ID: {owner.owner_id}")
        print(f"Name    : {owner.name}")
        print(f"Contact : {owner.contact_number}")
    except ValueError as e:
        print(f"\n[ERROR] {e}")

def view_owners_flow(owner_service: OwnerManagement):
    print_header("Registered Pet Owners")
    owners = owner_service.get_all_owners()

    if not owners:
        print("No registered pet owners found.")
        return

    print(f"{'ID':<38} | {'NAME':<20} | {'CONTACT':<15}")
    print("-" * 77)
    for owner in owners:
        print(f"{owner.owner_id:<38} | {owner.name:<20} | {owner.contact_number:<15}")

def add_pet_flow(owner_service: OwnerManagement, pet_service: PetManagement):
    print_header("Add Pet Record")
    owner_id = input("Enter Owner ID: ").strip()

    # Validate owner existence before prompting for pet details
    owner = owner_service.get_owner_by_id(owner_id)
    if not owner:
        print(f"\n[ERROR] Owner with ID '{owner_id}' does not exist.")
        return

    print(f"Owner Found: {owner.name}")
    print("Supported Species: Dog, Cat, Bird, Rabbit")
    species = input("Enter Species: ").strip()
    name = input("Enter Pet Name: ").strip()
    age_input = input("Enter Pet Age (or press [ENTER] to skip): ").strip()

    age = None
    if age_input:
        try:
            age = int(age_input)
        except ValueError:
            print("\n[ERROR] Age must be a valid integer.")
            return

    try:
        pet = pet_service.add_pet(owner_id=owner.owner_id, pet_type=species, name=name, age=age)
        print(f"\n[SUCCESS] Pet record added successfully via PetFactory!")
        print(f"Pet ID  : {pet.pet_id}")
        print(f"Name    : {pet.name}")
        print(f"Species : {pet.species}")
        print(f"Age     : {pet.age}")
        print(f"Owner   : {owner.name} ({owner.owner_id})")
    except ValueError as e:
        print(f"\n[ERROR] {e}")

def view_pets_flow(pet_service: PetManagement):
    print_header("Clinic Pet Records")
    pets = pet_service.get_all_pets()

    if not pets:
        print("No registered pets found.")
        return

    print(f"{'PET ID':<38} | {'NAME':<15} | {'SPECIES':<10} | {'OWNER ID':<38}")
    print("-" * 107)
    for pet in pets:
        print(f"{pet.pet_id:<38} | {pet.name:<15} | {pet.species:<10} | {pet.owner_id:<38}")

def schedule_appointment_flow(pet_service: PetManagement, appt_service: AppointmentManagement):
    print_header("Schedule Appointment")
    pet_id = input("Enter Pet ID: ").strip()

    pet = pet_service.get_pet_by_id(pet_id)
    if not pet:
        print(f"\n[ERROR] Pet with ID '{pet_id}' does not exist.")
        return

    print(f"Pet Found: {pet.name} ({pet.species})")
    date = input("Enter Date (e.g. YYYY-MM-DD): ").strip()
    time = input("Enter Time (e.g. 10:00 AM or 14:30): ").strip()
    reason = input("Enter Reason for Visit: ").strip()

    try:
        appt = appt_service.schedule_appointment(
            pet_id=pet.pet_id, date=date, time=time, reason=reason
        )
        print(f"\n[SUCCESS] Appointment booked successfully!")
        print(f"Appointment ID : {appt.appointment_id}")
        print(f"Pet Name       : {pet.name}")
        print(f"Date & Time    : {appt.date} at {appt.time}")
        print(f"Status         : {appt.status}")
    except ValueError as e:
        print(f"\n[ERROR] {e}")

def view_appointments_flow(appt_service: AppointmentManagement):
    print_header("Appointment Schedules")
    status_filter = input(
        "Filter by status (Scheduled, Completed, Cancelled) or press [ENTER] for all: "
    ).strip()

    try:
        appointments = appt_service.get_appointments(
            status=status_filter if status_filter else None
        )
    except ValueError as e:
        print(f"\n[ERROR] {e}")
        return

    if not appointments:
        print("No appointments found.")
        return

    print(f"{'APPOINTMENT ID':<38} | {'DATE':<12} | {'TIME':<10} | {'STATUS':<12} | {'REASON'}")
    print("-" * 90)
    for appt in appointments:
        print(f"{appt.appointment_id:<38} | {appt.date:<12} | {appt.time:<10} | {appt.status:<12} | {appt.reason}")

def cancel_appointment_flow(appt_service: AppointmentManagement):
    print_header("Cancel Appointment")
    appointment_id = input("Enter Appointment ID to cancel: ").strip()

    try:
        cancelled = appt_service.cancel_appointment(appointment_id)
        if cancelled:
            print(f"\n[SUCCESS] Appointment '{appointment_id}' has been cancelled.")
        else:
            print(f"\n[ERROR] Appointment with ID '{appointment_id}' was not found.")
    except ValueError as e:
        print(f"\n[ERROR] {e}")

def main():
    # Initialize the Singleton Database instance
    db = ClinicDatabase("clinic.db")

    # Initialize domain services
    owner_service = OwnerManagement(db)
    pet_service = PetManagement(db)
    appt_service = AppointmentManagement(db)

    while True:
        print_header("Paws & Care Clinic Management System")
        print("1. Register Pet Owner")
        print("2. View Registered Pet Owners")
        print("3. Add Pet Record")
        print("4. View Pet Records")
        print("5. Schedule Appointment")
        print("6. View Appointments")
        print("7. Cancel Appointment")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ").strip()

        match choice:
            case "1":
                register_owner_flow(owner_service)
            case "2":
                view_owners_flow(owner_service)
            case "3":
                add_pet_flow(owner_service, pet_service)
            case "4":
                view_pets_flow(pet_service)
            case "5":
                schedule_appointment_flow(pet_service, appt_service)
            case "6":
                view_appointments_flow(appt_service)
            case "7":
                cancel_appointment_flow(appt_service)
            case "8":
                print("\nShutting down system. Goodbye!")
                db.close()
                sys.exit(0)
            case _:
                print("\n[INVALID] Please select a valid option from 1 to 8.")

if __name__ == "__main__":
    main()