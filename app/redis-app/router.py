from app.database import redis

from fastapi import APIRouter


router = APIRouter(
    prefix="/{{app_name}}",
    tags=["{{app_name}}"],
    responses={404: {"description": "Not found"}},
)
