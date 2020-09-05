from typing import Dict, Optional
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_CONNECTION_STRING: Optional[str] = None

    @validator("DB_CONNECTION_STRING", pre=True)
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, str]) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER") or "",
            password=values.get("DB_PASSWORD") or "",
            host=values.get("DB_HOST") or "",
            path=f"/{values.get('DB_NAME') or ''}",
        )
