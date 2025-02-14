from passlib.hash import pbkdf2_sha256





def hash_password(password: str) -> str:
    """
    Hash a plain-text password using pbkdf2_sha256.
    
    Args:
        password (str): The plain-text password.
        
    Returns:
        str: The hashed password.
    """
    return pbkdf2_sha256.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against the hashed password.
    
    Args:
        plain_password (str): The plain-text password to verify.
        hashed_password (str): The hashed password stored in your database.
        
    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pbkdf2_sha256.verify(plain_password, hashed_password)
