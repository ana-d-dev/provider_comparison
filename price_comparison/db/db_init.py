from price_comparison.db.engine import engine, metadata


def create_tables():
    metadata.create_all(engine)