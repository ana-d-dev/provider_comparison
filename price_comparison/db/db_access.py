from price_comparison.db.tables import tariffs, users
from price_comparison.db.engine import engine
from sqlalchemy import select


def get_all_data():
    with engine.connect() as conn:
        result = conn.execute(select(tariffs))
        rows = result.mappings().all()

    clean_rows = []
    for row in rows:
        clean_row = {key: (value if value is not None else '-') for key, value in row.items()}
        clean_rows.append(clean_row)
    return clean_rows


def get_provider_data(provider_name):
    if not provider_name:
        raise ValueError("provider_name must be a non-empty string")

    with engine.connect() as conn:
        result = conn.execute(select(tariffs).where(tariffs.c.provider == provider_name))
        rows = result.mappings().all()

    clean_rows = []
    for row in rows:
        clean_row = {key: (value if value is not None else '-') for key, value in row.items()}
        clean_rows.append(clean_row)
    return clean_rows


def is_username_taken(username):
    with engine.connect() as conn:
        user = conn.execute(select(users).where(users.c.username == username)).first()
        if user:
            return True # Username is taken
        else:
            return False # Username is available


def is_api_taken(api_key):
    with engine.connect() as conn:
        api = conn.execute(select(users).where(users.c.api_key == api_key)).first()
        if api:
            return True # API_KEY is taken
        else:
            return False # API_KEY is available


def get_user(username):
    with engine.connect() as conn:
        user = conn.execute(select(users).where(users.c.username == username)).mappings().first()
        return user


def get_user_by_id(user_id):
    with engine.connect() as conn:
        user = conn.execute(select(users).where(users.c.id == user_id)).mappings().first()
        return user


def get_user_by_api_key(api_key):
    with engine.connect() as conn:
        user =  conn.execute(select(users).where(users.c.api_key == api_key)).mappings().first()
        return user