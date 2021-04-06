from typing import Type

from fastapi import HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from pydantic import BaseModel


class ErrorMessage(BaseModel):
    """
    Generic error class. This class is needed only for openapi documentation
    purposes.

    If some field in additional http errors changes, these changes
    should be reflected in the error model.

    Attributes:
    -----------

    detail:
        The error message

    """

    detail: str


class UnauthorizedError(HTTPException):
    """Unauthorized error"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InactiveUserError(HTTPException):
    """Inactive user error """

    def __init__(self):
        super().__init__(status_code=400, detail="Inactive user")


class ForbiddenOperationError(HTTPException):
    """Forbidden operation"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Operation not allowed"
        )


class EntityNotFoundError(HTTPException):
    """Error raised when entity not found"""

    def __init__(self, name: str, type: Type):
        self.name = name
        self.type = Type

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found entity {name} of type {type.__name__}",
        )


class GenericError(HTTPException):
    """Generic error"""

    def __init__(self, exception: Exception):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exception)
        )


async def common_exception_handler(request: Request, error: Exception):
    """Wraps errors as custom generic error"""
    return await http_exception_handler(request, GenericError(error))
