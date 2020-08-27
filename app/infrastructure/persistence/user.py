from sqlalchemy import Column, Integer, String, Table
from app.infrastructure.persistence.base_metadata import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(16), unique=True),
    Column("email", String(50), unique=True),
)
