from pydantic_settings import BaseSettings
from functools import lru_cache
import os


CLIENT_ID = os.environ.get('clientId')
CLIENT_SECRET = os.environ.get('secret')

class Settings(BaseSettings):
    names: str = "FittedAPI"
    db_client_id: str = CLIENT_ID
    db_client_secret: str = CLIENT_SECRET


@lru_cache
def get_settings():
    return Settings()