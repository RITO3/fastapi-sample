from sqlalchemy import Column, String, Table
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.persistence.base_metadata import metadata

users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("username", String(16), unique=True, nullable=False),
    Column("email", String(50), unique=True, nullable=False),
    Column("first_name", String(16), nullable=False),
    Column("last_name", String(16), nullable=False),
)
