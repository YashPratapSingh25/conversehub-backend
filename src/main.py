from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded
from fastapi.exceptions import RequestValidationError
from src.core.limiter import limiter
from src.auth.routes.__init__ import auth_router
import src.auth.models.__init__
from src.conversation.routers.__init__ import conversation_router
import src.conversation.models.__init__ 
from src.core.db import engine
from src.core.exceptions_utils.exception_handlers import (
    app_exception_handler,
    global_exception_handler,
    rate_limit_exception_handler,
    request_validation_handler,
    http_exception_handler
)
from src.core.exceptions_utils.exceptions import AppException
from src.core.middlewares.logging_middleware import LoggingMiddleware
from src.core.scheduler import close_scheduler, init_scheduler
from src.core.logger import logger

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(conversation_router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

app.add_middleware(LoggingMiddleware)

