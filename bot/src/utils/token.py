from jose import ExpiredSignatureError, JWTError, jwt
import os
from exceptions import IncorrectTokenException
from datetime import datetime, timedelta


SECRET_KEY: str = os.getenv('SECRET_KEY')
ALGORITHM: str = os.getenv('ALGORITHM')


def valid_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except ExpiredSignatureError:
        return None
    except JWTError:
        raise IncorrectTokenException
    return payload



def create_session_token(data: dict) -> str:
    to_encode: dict = data.copy()
    expire: datetime = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encode_jwt