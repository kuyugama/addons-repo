import bcrypt


def make(payload: str) -> str:
    return bcrypt.hashpw(payload.encode(), bcrypt.gensalt()).decode()


def verify(payload: str, secret_hash: str) -> bool:
    return bcrypt.checkpw(payload.encode(), secret_hash.encode())
