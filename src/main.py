from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded
from fastapi.exceptions import RequestValidationError
from src.core import limiter
from src.core.db import engine, async_sessionmaker
from src.auth.__init__ import auth_router
from src.core.exceptions_utils.exception_handlers import (
    app_exception_handler,
    global_exception_handler,
    rate_limit_exception_handler,
    request_validation_handler,
    http_exception_handler
)
from src.core.exceptions_utils.exceptions import AppException

@asynccontextmanager
async def lifespan(app : FastAPI):
    app.state.engine = engine
    app.state.async_sessionmaker = async_sessionmaker
    app.state.limiter = limiter

    yield

    await app.state.engine.dispose()

app = FastAPI(lifespan=lifespan, title="ConverseHub Backend")

app.include_router(auth_router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)