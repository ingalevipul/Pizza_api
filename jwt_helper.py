import jwt
from datetime import datetime, timedelta
from schemas import Settings

settings = Settings()

class JWTHelper:
    @staticmethod
    def create_access_token(subject: str):
        expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
        encoded_jwt = jwt.encode(to_encode, settings.authjwt_secret_key, algorithm="HS256")
        return encoded_jwt

    @staticmethod
    def create_refresh_token(subject: str):
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
        encoded_jwt = jwt.encode(to_encode, settings.authjwt_secret_key, algorithm="HS256")
        return encoded_jwt
