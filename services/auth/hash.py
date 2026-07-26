import hashlib

from passlib.hash import bcrypt


def hash_pass(password: str):
    hash = bcrypt.hash(password)
    return hash


def verify_password(password: str, hashed_password: str):
    return bcrypt.verify(password, hashed_password)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
