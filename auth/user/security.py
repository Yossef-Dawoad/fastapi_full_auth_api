from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
SPECIAL_CHARCTERS = list('@#$%+:?>.<\\|/~, ')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_str_hash(password: str) -> str:
    return pwd_context.hash(password)

def is_password_strong(password: str) -> bool:
    if not any(ch.isupper for ch in password): return False
    if not any(ch.islower for ch in password): return False
    if not any(ch.isdigit for ch in password): return False
    if not any(ch in SPECIAL_CHARCTERS for ch in password): return False

    return True
