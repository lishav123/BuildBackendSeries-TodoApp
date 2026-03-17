import bcrypt

def get_password_hash(password: str) -> str:
    """Hashes a plaintext password using bcrypt."""
    # bcrypt requires passwords to be bytes, so we encode the string
    pwd_bytes = password.encode('utf-8')

    # Generate a random salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)

    # Decode back to a string so it can be saved in your MongoDB User model
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a plaintext password matches the hashed one in the database."""
    # Convert both to bytes for bcrypt to compare
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')

        return bcrypt.checkpw(password_bytes, hashed_password_bytes)
    except:
        return False