from functools import lru_cache
from typing import Any, Dict, Optional
import urllib.parse
from pydantic import BaseSettings, Field, validator
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_TYPE: str = Field(default="sqlite", env="DB_TYPE")
    HOST: str = Field(default="localhost", env="PGDB_HOST")
    USER: str = Field(default="root", env="PGDB_USER")
    PASSWORD: str = Field(default="", env="PGDB_PASSWORD")
    DB: str = Field(default="test_db", env="PGDB_DB")
    PORT: int = Field(default=3306, env="PGDB_PORT")
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True, always=True)
    def assemble_db_connection(cls, v, values: Dict[str, Any]) -> str:
        db_type = values.get("DB_TYPE", "sqlite").lower()
        user = values.get("USER")
        password = urllib.parse.quote(values.get("PASSWORD", ""))
        host = values.get("HOST")
        port = values.get("PORT")
        db = values.get("DB")

        if db_type == "mysql":
            return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
        elif db_type == "postgresql":
            return f"postgresql://{user}:{password}@{host}:{port}/{db}"
        else:
            return f"sqlite:///./{db}.db"

@lru_cache()
def get_settings():
    return Settings()
