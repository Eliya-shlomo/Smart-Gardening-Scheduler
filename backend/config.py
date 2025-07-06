import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

## config file for app. 
## variables for db and alembic.
## variables from .env os loaded here for the alembic to read them on run time.
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))
load_dotenv(dotenv_path=env_path)

required_keys = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "DATABASE_URL"]
for key in required_keys:
    value = os.getenv(key)
    if value:
        os.environ[key] = value

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str
    SECRET_KEY: str = "supersecret"
    MAIL_FROM: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()
