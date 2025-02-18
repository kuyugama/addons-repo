from src.error import define_error_category

define_error = define_error_category("auth")

invalid_secret = define_error("invalid-secret", "Invalid secret", status_code=403)
invalid_key = define_error("invalid-key", "Invalid public key", status_code=400)
no_user = define_error("no-user", "No user", status_code=404)
already_exists = define_error("user-already-exists", "User already exists", status_code=400)
