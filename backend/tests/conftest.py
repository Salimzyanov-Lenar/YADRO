import pytest
import asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.database import get_db, Base
from src.users.models import User


DATABASE_URL = "sqlite+aiosqlite:///:memory:"


engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)


AsyncSessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def setup_and_teardown():
    async def setup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with AsyncSessionLocal() as session:
            session.add_all([
                User(
                    gender="male",
                    first_name="Ivan",
                    second_name="Ivanov",
                    phone_number="1234567890",
                    email="ivan@example.com",
                    residing_place="Moscow",
                    photo_url="http://example.com/photo1.jpg"
                ),
                User(
                    gender="female",
                    first_name="Anna",
                    second_name="Petrova",
                    phone_number="0987654321",
                    email="anna@example.com",
                    residing_place="Saint Petersburg",
                    photo_url="http://example.com/photo2.jpg"
                ),
                User(
                    gender="male",
                    first_name="Chill",
                    second_name="Guy",
                    phone_number="0987654321",
                    email="chillguy@example.com",
                    residing_place="Bali",
                    photo_url="http://example.com/photo3.jpg"
                )
            ])
            await session.commit()

    async def teardown():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(setup())
    yield
    asyncio.run(teardown())


@pytest.fixture(scope="module")
def client():
    return TestClient(app)
