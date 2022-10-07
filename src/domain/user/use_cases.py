from datetime import datetime, timedelta

from passlib.context import CryptContext

from src.data.repos.user import UserRepo, UserAuthRepo
from src.domain.user.dto.base import UserBaseSchema, UserCreateSchema


class UserUseCase:

    def __init__(self, repo: UserRepo):
        self.repo = repo

    async def get_all(self):
        return await self.repo.get_all()


class UserAuthUseCase:

    def __init__(self, user_repo: UserRepo, user_auth_repo: UserAuthRepo):
        self.user_repo = user_repo
        self.user_auth_repo = user_auth_repo
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register(self, user: UserCreateSchema):
        user.password = self.get_password_hash(user.password)
        return await self.user_auth_repo.create(data=user.dict())

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_repo.get_user_by_username(username)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    def create_access_token(self, data: dict):
        return self.user_auth_repo.create_access_token(data=data)

    async def get_current_user(self, token: str) -> UserBaseSchema:
        return await self.user_auth_repo.get_current_user(token=token)

    async def login_for_access_token(self, username: str, password: str):
        user = await self.authenticate_user(username, password)
        if not user:
            return False
        access_token_expires = timedelta(minutes=15)
        access_token = self.create_access_token(
            data={"sub": user.username, "exp": datetime.utcnow() + access_token_expires}
        )
        return access_token

