import sqlite3
from database import ClinicDatabase
from models import Owner

class OwnerManagement:
    """Service layer handling business logic for Pet Owners."""

    def __init__(self, db):
        self.db = db or ClinicDatabase()

    def register_owner(self, name, contact_number):
        """Creates and stores a new pet owner.

        Args:
            name: Full name of the pet owner.
            contact_number: Contact phone number (used for deterministic ID generation).

        Returns:
            Owner: The created Owner domain instance.

        Raises:
            ValueError: If input validation fails or if the owner already exists.
        """
        clean_name = name.strip()
        clean_contact = str(contact_number).strip()

        if not clean_name:
            raise ValueError("Owner name cannot be empty.")
        if not clean_contact:
            raise ValueError("Contact number cannot be empty.")

        owner = Owner(name=clean_name, contact_number=clean_contact)

        query = """
            INSERT INTO owners (owner_id, name, contact_number)
            VALUES (?, ?, ?)
        """
        try:
            self.db.execute_query(
                query, (owner.owner_id, owner.name, owner.contact_number)
            )
        except sqlite3.IntegrityError:
            raise ValueError(
                f"An owner with ID '{owner.owner_id}' (contact: {clean_contact}) already exists."
            )

        return owner

    def get_owner_by_id(self, owner_id):
        """Retrieves a single owner by their UUID.

        Args:
            owner_id: The UUID string of the owner.

        Returns:
            Owner instance if found, None otherwise.
        """
        query = "SELECT owner_id, name, contact_number FROM owners WHERE owner_id = ?"
        row = self.db.fetch_one(query, (owner_id,))

        if not row:
            return None

        return Owner(
            name=row["name"],
            contact_number=row["contact_number"],
            owner_id=row["owner_id"],
        )

    def get_all_owners(self):
        """Retrieves all registered pet owners.

        Returns:
            List of Owner instances.
        """
        query = "SELECT owner_id, name, contact_number FROM owners ORDER BY name ASC"
        rows = self.db.fetch_all(query)

        return [
            Owner(
                name=row["name"],
                contact_number=row["contact_number"],
                owner_id=row["owner_id"],
            )
            for row in rows
        ]