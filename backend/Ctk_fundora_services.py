from database.Ctk_fundora_auth import register_user

def process_register(data: dict) -> str:
    # 1. Grundlæggende validering
    required_fields = ["fornavn", "efternavn", "telefon", "email", "password", "password_gentag"]
    for field in required_fields:
        if not data.get(field):
            return "missing_fields"

    if data["password"] != data["password_gentag"]:
        return "password_mismatch"

    if not data.get("tillad_data"):
        return "no_data_consent"

    # 2. Kald register_user fra auth.py
    result = register_user(
        email=data["email"],
        password=data["password"],
        fornavn=data["fornavn"],
        efternavn=data["efternavn"],
        telefon=data["telefon"],
        tillad_data=data["tillad_data"],
        vil_kontaktes=data["vil_kontaktes"]
    )

    return result  # "success", "email_exists", "db_error", etc.
