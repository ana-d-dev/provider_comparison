from sqlalchemy import insert, delete
from price_comparison.db.engine import engine
from price_comparison.db.tables import tariffs
from price_comparison.db.tables import users



def refresh_db():
    """
    Delete all rows from the 'tariffs' table.

    This function performs a full cleanup of the tariffs table.
    It does not drop the table, only removes all existing records.
    """
    with engine.begin() as conn:
        conn.execute(delete(tariffs))


def save_to_db(data):
    """
    Insert a list of tariff dictionaries into the 'tariffs' table.

    Pre-processing:
    - Converts empty string values ('') into None (stored as NULL in DB)

    Args:
        data (list[dict]): List of tariff records to insert.

    Behavior:
    - Executes a bulk insert into the tariffs table.
    - Uses a transaction (engine.begin) to ensure atomic commit.
    """
    for row in data:
        for key, value in row.items():
            if value == '':
                row[key] = None


    stmt = insert(tariffs).values(data)
    with engine.begin() as conn:
        conn.execute(stmt)


def save_user(new_user):
    """
    Insert a new user record into the 'users' table.

    Args:
        new_user (dict):
            Dictionary containing user data with keys:
            - username (str)
            - hashed_password (str)
            - api_key (str)

    Behavior:
    - Executes a single insert operation into the users table.
    - Uses a transaction to ensure the write is committed safely.
    """
    stmt = insert(users).values(new_user)
    with engine.begin() as conn:
        conn.execute(stmt)