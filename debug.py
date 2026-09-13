from database import ClinicDatabase
from services.OwnerManagement import OwnerManagement
from services.PetManagement import PetManagement

# 1. Reset singleton
ClinicDatabase.reset_instance()

# 2. Create in-memory database
db = ClinicDatabase(":memory:")

# 3. Print existing tables directly from SQLite schema
cursor = db.connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print(f"Tables found in db instance: {tables}")

# 4. Check services
owner_mgr = OwnerManagement(db)
pet_mgr = PetManagement(db)
print(f"PetManagement using same DB instance: {pet_mgr.db is db}")
print(f"PetManagement connection object: {pet_mgr.db.connection}")