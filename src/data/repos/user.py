from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import JWTError, jwt
from sqlalchemy import select
from starlette import status

from src.common.repository import BaseRepo
from src.data.models.user.user import User
from src.domain.user.dto.base import UserOutSchema


class BaseUserRepo(BaseRepo):
    model = User
    query = select(User).where(User.is_active == True)
    schema = UserOutSchema


class UserRepo(BaseUserRepo):
    ...


class UserAuthRepo(BaseUserRepo):
    def __init__(self, db, config: dict):
        super().__init__(db)
        self.access_token_expire_minutes = config.get("access_token_expire_minutes")
        self.refresh_token_expire_days = config.get("refresh_token_expire_days")
        self.secret_key = config.get("secret_key")
        self.algorithm = config.get("algorithm")

    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        token_type = to_encode.get("type")
        if token_type == "access":
            expires_delta = timedelta(minutes=self.access_token_expire_minutes)
        else:
            expires_delta = timedelta(days=self.refresh_token_expire_days)

        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm,
        )
        return encoded_jwt

    async def get_current_user(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
            username: str = payload.get("sub")
            token_type: str = payload.get("type")
            exp: datetime = payload.get("exp")
            if username is None or token_type != "access" or exp < datetime.utcnow().timestamp():
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await self.get_one(username, "username")
        if user is None:
            raise credentials_exception
        return user

    async def refresh_token(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
            username: str = payload.get("sub")
            token_type: str = payload.get("type")
            exp: datetime = payload.get("exp")
            if username is None or token_type != "refresh" or exp < datetime.utcnow().timestamp():
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await self.get_one(username, "username")
        if user is None:
            raise credentials_exception
        return user
