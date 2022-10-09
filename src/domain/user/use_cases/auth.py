from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import SecretStr

from src.data.repos.user import UserAuthRepo
from src.domain.user.dto.auth import Token
from src.domain.user.dto.base import UserBaseSchema, UserCreateSchema


class UserAuthUseCase:
    def __init__(
        self,
        user_auth_repo: UserAuthRepo,
    ) -> None:
        self.user_auth_repo = user_auth_repo
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register(self, user: UserCreateSchema) -> UserBaseSchema:
        user.password = self.get_password_hash(user.password)
        return await self.user_auth_repo.create(data=user.dict())

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: SecretStr) -> str:
        return self.pwd_context.hash(password.get_secret_value())

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_auth_repo.get_one(username, "username")

        if not self.verify_password(password, user.password.get_secret_value()):
            raise HTTPException(status_code=400, detail="Incorrect password")
        return user

    def create_token(self, data: dict) -> str:
        return self.user_auth_repo.create_token(data=data)

    def create_access_refresh_token(self, user):
        access_token = self.create_token(
            data={"sub": user.username, "role": user.role, "type": "access"}
        )

        refresh_token = self.create_token(
            data={"sub": user.username, "role": user.role, "type": "refresh"}
        )
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    async def get_current_user(self, token: str) -> UserBaseSchema:
        return await self.user_auth_repo.get_current_user(token=token)

    async def login_for_access_token(self, username: str, password: SecretStr):
        user = await self.authenticate_user(username, password)
        if not user:
            return False
        return self.create_access_refresh_token(user)

    async def refresh_token(self, token: str):
        user = await self.user_auth_repo.refresh_token(token=token)
        if not user:
            return False
        return self.create_access_refresh_token(user)
