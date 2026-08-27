from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from app.database import check_database_connection, engine
from app.routers.items import router as items_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    await check_database_connection()
    try:
        yield
    finally:
        await engine.dispose()


async def database_unavailable(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(status_code=503, content={"detail": "Database unavailable"})


def create_app() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_exception_handler(OperationalError, database_unavailable)
    application.include_router(items_router)
    return application