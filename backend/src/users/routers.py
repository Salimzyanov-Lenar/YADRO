from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.users.schemas import ExternalResponse, UserResponseModel
from src.users.services import transform_user


router = APIRouter()

