from dotenv import load_dotenv
from pathlib import Path
import os


from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


load_dotenv(dotenv_path=Path('../../.env'))


PASSWORD_SECRET_HASH: str = os.getenv(
    "PASSWORD_SECRET_HASH") or "{{PASSWORD_SECRET_HASH}}"


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET") or "{{JWT_SECRET}}"
    authjwt_algorithm: str = os.getenv("ALGORITHMS") or "HS256"

    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config() -> Settings:
    return Settings()
