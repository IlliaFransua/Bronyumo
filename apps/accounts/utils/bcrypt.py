import bcrypt


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    :param password: The password to be hashed.
    :return: The hashed password as a string.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if the provided plain password matches the hashed password.

    :param plain_password: The password entered by the user.
    :param hashed_password: The hashed password to compare against.
    :return: True if the passwords match, otherwise False.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))