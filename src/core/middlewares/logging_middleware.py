from datetime import datetime
import time
from uuid import uuid4, UUID
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.auth.models.user_model import UserAuth
from src.core.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request : Request, call_next):
        start_time = time.time()
        request_id = str(uuid4())
        request.state.user = "anonymous"

        logger.bind(
            request_id = request_id,
            method = request.method,
            path = request.url.path,
            timestamp = datetime.now()
        ).info(f"Request: {request_id} - {request.method} {request.url.path}")

        request.state.request_id = request_id
        
        response = await call_next(request)

        duration = time.time() - start_time

        try:
            user_id = request.state.user
        except:
            user_id = None

        logger.bind(
            request_id = request_id,
            method = request.method,
            path = request.url.path,
            timestamp = datetime.now(),
            user_id = user_id,
            duration = duration,
            status_code = response.status_code
        ).info(f"Response: {request_id} - {request.method} {request.url.path}")

        return response