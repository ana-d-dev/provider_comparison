"""
Database table definitions for the application.

This module defines SQLAlchemy Table objects used to represent
the database schema for the project.

It includes:
- tariffs: stores mobile tariff offers from different providers
- users: stores registered users, authentication data, and API keys

Both tables are attached to the shared metadata object from db.engine
and are used for schema creation and query building.
"""
from sqlalchemy import Column, Integer, String, Date, Table, DateTime, func
from price_comparison.db.engine import metadata

tariffs = Table (
    'tariffs',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('scraped_date', Date),
    Column('provider', String),
    Column('name', String),
    Column('price', String),
    Column('gb', String),
    Column('minutes', String),
    Column('sms', String),
    Column('units', String),
    Column('one_gb_price', String),
    Column('sixty_min_price', String),
    Column('thousand_units', String)
)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, unique=True, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('api_key', String, unique=True, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
)