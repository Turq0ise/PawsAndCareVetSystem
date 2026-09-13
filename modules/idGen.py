import uuid
ROOT_NAMESPACE = uuid.NAMESPACE_X500
OWNER_NAMESPACE = uuid.uuid5(ROOT_NAMESPACE, "OWNER")
PET_NAMESPACE = uuid.uuid5(ROOT_NAMESPACE, "PET")
APPOINTMENT_NAMESPACE = uuid.uuid5(ROOT_NAMESPACE, "APPOINTMENT")

def idGen(value, context):
    value = str(value).upper()

    match context.upper():
        case "OWNER" | "OWNERS":
            return str(uuid.uuid5(OWNER_NAMESPACE, value))
        case "PET" | "PETS":
            return str(uuid.uuid5(PET_NAMESPACE, value))
        case "APPOINTMENT" | "APPOINTMENTS":
            return str(uuid.uuid5(APPOINTMENT_NAMESPACE, value))
        case _:
            raise ValueError(
                f"Invalid context '{context}'. Expected 'OWNER', 'PET', or 'APPOINTMENT'."
            )
