from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.users.routers import router as users_router
from src.database import Base, engine, async_session
from src.users.services import load_fetched_users_to_db, delete_all_users
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # async with async_session() as session:
    #     await load_fetched_users_to_db(session, total_users=1000) 
    
    yield
    
    # async with async_session() as session:
    #     await delete_all_users(session)


docs_url = "/docs" if settings.DEBUG else None
redoc_url = "/redoc" if settings.DEBUG else None
openapi_url = "/openapi.json" if settings.DEBUG else None


app = FastAPI(
    lifespan=lifespan,
    debug=settings.DEBUG,
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://localhost:3000",
        ],
    allow_credentials=True,
    allow_methods=['GET'],
    allow_headers=['*'],
)

# "/api/users/v1/.."
app.include_router(users_router)

