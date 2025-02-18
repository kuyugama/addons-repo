from src.error import define_error

token_invalid = define_error("auth", "token-invalid", "Token invalid", 401)
token_expired = define_error("auth", "token-expired", "Token expired", 403)
