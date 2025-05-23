from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from src.users.models import User
from src.users.schemas import ExternalUser, UserCreateModel
from src.users.fetch_users import fetch_users


async def save_user_to_db(user: UserCreateModel, db: AsyncSession):
    new_user = User(
        gender = user.gender,
        first_name = user.first_name,
        second_name = user.second_name,
        phone_number = user.phone_number,
        email = user.email,
        residing_place = user.residing_place,
        photo_url = user.photo_url
    )
    db.add(new_user)
    await db.commit()


def transform_user(user: ExternalUser) -> UserCreateModel:
    """
    Transform External User from API for our service
    """
    return UserCreateModel(
        gender=user.gender,
        first_name=user.name.first,
        second_name=user.name.last,
        phone_number=user.phone,
        email=user.email,
        residing_place=f"{user.location.city}, {user.location.country}",
        photo_url=user.picture.medium
    )


async def load_fetched_users_to_db(db: AsyncSession, total_users: int = 1000, batch_size: int = 100):
    """
    Function for call fetching and then save the response to DB
    """
    from src.users.services import transform_user, save_user_to_db

    for _ in range(total_users // batch_size):
        external_response = await fetch_users(batch_size)
        for external_user in external_response.results:
            user = transform_user(external_user)
            await save_user_to_db(user, db)


async def delete_all_users(session: AsyncSession) -> None:
    """
    Deleting all users from table users after application shutdown
    """
    await session.execute(delete(User))
    await session.commit()