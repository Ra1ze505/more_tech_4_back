
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.containers.container import container
from src.domain.user.dto.base import oauth2_scheme, UserCreateSchema, Token
from src.domain.user.use_cases import UserAuthUseCase, UserUseCase

user_router = APIRouter(prefix='/user', tags=['user'])


@user_router.get("/all")
async def get_all(
):
    service: UserUseCase = container.use_cases.user()
    return await service.get_all()


@user_router.post("/register")
async def register(
    user: UserCreateSchema,
):
    service: UserAuthUseCase = container.use_cases.user_auth()
    return await service.register(user)


@user_router.post("/token", response_model=Token)
async def login_for_access_token(
    user: OAuth2PasswordRequestForm = Depends(),
):
    service: UserAuthUseCase = container.use_cases.user_auth()
    return await service.login_for_access_token(user.username, user.password)


@user_router.post("/token/refresh", response_model=Token)
async def refresh_token(
    token: str
):
    service: UserAuthUseCase = container.use_cases.user_auth()
    return await service.refresh_token(token)


@user_router.get("/me")
async def me(
    token: str = Depends(oauth2_scheme)
):
    service: UserAuthUseCase = container.use_cases.user_auth()
    return await service.get_current_user(token)
