from src.error import define_error_category

define_error = define_error_category("addon")

not_found = define_error("not-found", "Addon not found", 404)
version_not_found = define_error("version-not-found", "Addon version not found", 404)

invalid_package = define_error("invalid-package", "Invalid addon package", 400)
invalid_meta = define_error("invalid-metadata", "Invalid addon metadata", 400)
already_exists = define_error("already-exists", "Addon already exists", 409)
invalid_file = define_error_category("system")("invalid-file", "Invalid file", 500)

not_owner = define_error("not-owner", "Not owner", 403)
