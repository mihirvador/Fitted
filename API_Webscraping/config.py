import pathlib
import json
from pydantic_settings import BaseSettings
from functools import lru_cache

BASE_DIR = pathlib.Path(__file__).parent
TOKEN_JSON = str(BASE_DIR / "ignored" / "mihirrocks9999@gmail.com-token.json")

with open(TOKEN_JSON) as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

class Settings(BaseSettings):
    names: str = "FittedAPI"
    db_client_id: str = CLIENT_ID
    db_client_secret: str = CLIENT_SECRET


@lru_cache
def get_settings():
    return Settings()