from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


# JWT token
class TokenExpiredException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк"


class TokenAbsentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"

