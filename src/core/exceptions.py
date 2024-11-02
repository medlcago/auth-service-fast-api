from http import HTTPStatus

from fastapi.requests import Request
from fastapi.responses import JSONResponse


class APIException(Exception):
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR.value
    message: str = HTTPStatus.INTERNAL_SERVER_ERROR.phrase
    description: str = HTTPStatus.INTERNAL_SERVER_ERROR.description

    def __str__(self) -> str:
        return f"<{self.status_code} - {self.message}>: {self.description}"

    @property
    def details(self):
        return {
            "status_code": self.status_code,
            "message": self.message,
            "description": self.description,
        }


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:  # noqa
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.details
    )


class InvalidCredentialsException(APIException):
    status_code = HTTPStatus.UNAUTHORIZED.value
    message = HTTPStatus.UNAUTHORIZED.phrase
    description = HTTPStatus.UNAUTHORIZED.description


class UserAlreadyExistsException(APIException):
    status_code = HTTPStatus.CONFLICT.value
    message = HTTPStatus.CONFLICT.phrase
    description = HTTPStatus.CONFLICT.description
