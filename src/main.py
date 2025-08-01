from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded
from fastapi.exceptions import RequestValidationError
from src.core.limiter import limiter
from src.auth.__init__ import auth_router
from src.core.db import engine
from src.core.exceptions_utils.exception_handlers import (
    app_exception_handler,
    global_exception_handler,
    rate_limit_exception_handler,
    request_validation_handler,
    http_exception_handler
)
from src.core.exceptions_utils.exceptions import AppException
from src.core.scheduler import close_scheduler, init_scheduler

@asynccontextmanager
async def lifespan(app : FastAPI):
    await init_scheduler()
    app.state.engine = engine
    app.state.limiter = limiter

    yield

    await app.state.engine.dispose()
    limiter.enabled = False
    await close_scheduler()

app = FastAPI(lifespan=lifespan, title="ConverseHub Backend")

app.include_router(auth_router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)