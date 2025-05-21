from fastapi import APIRouter, Depends, Query, HTTPException

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.schemas import UserResponseModel
from src.users.models import User


router = APIRouter(
    prefix="/api/users/v1"
)


@router.get('', response_model = list[UserResponseModel])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: AsyncSession = Depends(get_db),
    ):

    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    users = result.scalars().all()

    return users


@router.get('/random/', response_model = UserResponseModel)
async def get_random_user(db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(User).order_by(func.random()).limit(1)
    )
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="No users found")

    return user