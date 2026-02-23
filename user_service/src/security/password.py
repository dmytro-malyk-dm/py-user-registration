from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=14,
    deprecated="auto"
)

def hash_password(password:str) -> str:
    """
    Hash a plain-text password using the configured password context.
    This function takes a plain-text password and returns its bcrypt hash.
    The bcrypt algorithm is used with a specified number of rounds for enhanced security.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against its hashed version.

    This function compares a plain-text password with a hashed password and returns True
    if they match, and False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
