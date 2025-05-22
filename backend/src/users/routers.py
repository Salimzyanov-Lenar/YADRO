from fastapi import APIRouter, Depends, Query, HTTPException

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.schemas import UserResponseModel, PaginatedUsersResponse
from src.users.models import User


router = APIRouter(
    prefix="/api/users/v1"
)


@router.get('', response_model=PaginatedUsersResponse)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: AsyncSession = Depends(get_db),
    ):

    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()

    total_query = await db.execute(select(func.count()).select_from(User))
    total_amount = total_query.scalar_one()
    has_next = skip + limit < total_amount

    return {
        "has_next": has_next,
        "total_amount": total_amount,
        "users": users,
    }


@router.get('/random/', response_model = UserResponseModel)
async def get_random_user(db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(User).order_by(func.random()).limit(1)
    )
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="No users found")

    return user