from fastapi.security import OAuth2PasswordBearer

from src.common.schema import BaseSchema
from src.data.models.user.user import UserRole


class Token(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseSchema):
    username: str | None = None
    role: UserRole | None = None


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/user/token",
)
