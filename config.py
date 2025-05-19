# config.py
# -------------------------
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    microsoft_app_id: str
    microsoft_app_password: str

    sql_server: str
    sql_database: str
    sql_username: str
    sql_password: str

    clu_endpoint: str
    clu_api_key: str
    clu_project: str
    clu_deployment: str

    class Config:
        env_file = ".env"

settings = Settings()
