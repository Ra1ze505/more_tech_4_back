from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import JWTError, jwt
from pydantic import parse_obj_as
from sqlalchemy import select
from starlette import status

from src.data.models.user import User
from src.data.repos.base import BaseRepo
from src.domain.user.dto.base import TokenData, UserBaseSchema


class BaseUserRepo(BaseRepo):
    model = User
    query = select(User)
    schema = UserBaseSchema
    out_schema = UserBaseSchema

    async def get_user_by_username(self, username: str) -> UserBaseSchema:
        stmt = select(User).where(User.username == username)
        user = (await self.session.execute(stmt)).scalars().one()
        return parse_obj_as(UserBaseSchema, user)


class UserRepo(BaseUserRepo):
    ...


class UserAuthRepo(BaseUserRepo):
    model = User
    query = select(User)
    schema = UserBaseSchema

    def __init__(self, db, config: dict):
        super().__init__(db)
        self.config = config

    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        token_type = to_encode.get("type")
        if token_type == "access":
            expires_delta = timedelta(minutes=self.config.get("access_token_expire_minutes"))
        else:
            expires_delta = timedelta(days=self.config.get("refresh_token_expire_days"))

        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.config.get("secret_key"),
            algorithm=self.config.get("algorithm"),
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
                self.config.get("secret_key"),
                algorithms=[self.config.get("algorithm")],
            )
            username: str = payload.get("sub")
            token_type: str = payload.get("type")
            exp: datetime = payload.get("exp")
            if username is None or token_type != "access" or exp < datetime.utcnow().timestamp():
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = await self.get_user_by_username(username=token_data.username)
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
                self.config.get("secret_key"),
                algorithms=[self.config.get("algorithm")],
            )
            username: str = payload.get("sub")
            token_type: str = payload.get("type")
            exp: datetime = payload.get("exp")
            if username is None or token_type != "refresh" or exp < datetime.utcnow().timestamp():
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = await self.get_user_by_username(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
