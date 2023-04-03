import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "My FastAPI Application"
    DEBUG: bool = bool(os.getenv("DEBUG", True))
    ALLOWED_HOSTS: list = os.getenv("ALLOWED_HOSTS", "").split(",")
    DATABASE_URL: str = os.getenv("DATABASE_URL", 'postgres+asyncpg://myuser:mypassword@localhost:5432/mydb')
    API_V1_PREFIX: str = os.getenv("API_V1_PREFIX", "v1")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SECRET_KEY")


settings = Settings()
