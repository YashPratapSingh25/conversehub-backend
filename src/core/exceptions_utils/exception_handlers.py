import json
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.core.common_schemas import ErrorModel
from src.core.exceptions_utils.exceptions import AppException
from slowapi.errors import RateLimitExceeded

def exception_helper(
    request : Request, 
    errors : list = None, 
    exc : HTTPException | RequestValidationError | AppException | None = None
) -> JSONResponse:
    
    error_detail = "Interal Server Error"
    status_code = 500

    if errors is None:
        if exc != None:
            error_detail = str(exc.detail)
            status_code = exc.status_code
    else:
        error_detail = errors
        status_code = 422

    error_response = ErrorModel(
        method = request.method,
        path = request.url.path,
        error = error_detail,
        status_code = status_code
    )
    return JSONResponse(
        status_code=error_response.status_code,
        content=error_response.model_dump(mode="json")
    )


def http_exception_handler(request : Request, exc : HTTPException):
    return exception_helper(request, exc=exc)

def request_validation_handler(request : Request, exc : RequestValidationError):
    sanitized_errors= []
    for error in exc.errors():
        if "ctx" in error and "error" in error["ctx"]:
            error["ctx"]["error"] = str(error["ctx"]["error"])

        sanitized_errors.append(error)

    return exception_helper(request, errors=sanitized_errors)

def global_exception_handler(request : Request, exc : Exception):
    print(f"DEBUG {exc}")
    return exception_helper(request)

def app_exception_handler(request : Request, exc : AppException):
    return exception_helper(request, exc=exc)

def rate_limit_exception_handler(request : Request, exc : RateLimitExceeded):
    return exception_helper(request, exc=exc)