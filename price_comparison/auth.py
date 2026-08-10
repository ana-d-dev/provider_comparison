from werkzeug.security import generate_password_hash, check_password_hash
from price_comparison.db.db_access import is_username_taken, is_api_taken, get_user
from price_comparison.db.sql_insert import save_user
import secrets

#  |-----------------------|
#  | REGISTRATION CHECKING |
#  |-----------------------|
# username availability
def check_username(username):
    """
    Check if a username is already taken.

    Args:
        username (str): Username to check.

    Returns:
        bool: True if username exists, False otherwise.
    """
    return is_username_taken(username)


# hash password
def hash_password(password):
    """
    Hash a plain-text password using Werkzeug security utilities.

    Args:
        password (str): Raw user password.

    Returns:
        str: Hashed password string.
    """
    hashed_password = generate_password_hash(password)
    return hashed_password


# generate new api key
def generate_api_key():
    """
    Generate a secure random API key.

    Returns:
        str: 64-character hexadecimal API key.
    """
    api_key = secrets.token_hex(32)
    return api_key


# create new user
def create_user(username, hashed_password, api_key):
    """
    Create a new user record and store it in the database.

    Args:
        username (str): Username of the new user.
        hashed_password (str): Hashed password.
        api_key (str): Generated API key.
    """
    new_user = {
        'username': username,
        'hashed_password': hashed_password,
        'api_key': api_key
    }
    save_user(new_user)


# registration of user
def register_user(username, password):
    """
    Register a new user if the username is not already taken.

    This function:
    - checks username availability
    - hashes the password
    - generates a unique API key
    - stores the user in the database

    Args:
        username (str): Desired username.
        password (str): Raw password.

    Returns:
        tuple:
            bool: Success status
            str: Message describing result
    """
    if not check_username(username):
        hashed_password = hash_password(password)
        while True:
            api_key = generate_api_key()
            if not is_api_taken(api_key):
                create_user(username, hashed_password, api_key)
                return True, 'Registration successful. You can now log in.'
    else:
        return False, 'Username is already taken, try another one.'


#  |----------------|
#  | LOGIN CHECKING |
#  |----------------|

# CHECK USERNAME AND PASSWORD
def auth_user(username, password):
    """
   Authenticate a user by verifying username and password.

   Args:
       username (str): Username input.
       password (str): Plain-text password input.

   Returns:
       dict | bool:
           User dictionary if authentication is successful,
           False otherwise.
   """
    user = get_user(username)
    if not user:
        return False

    if not check_password_hash(user['hashed_password'], password):
        return False

    return user
























