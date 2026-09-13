class ClinicDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.owners = {}
            cls._instance.pets = {}
            cls._instance.appointments = {}
        return cls._instance

    def clear_database(self):
        self.owners.clear()
        self.pets.clear()
        self.appointments.clear()