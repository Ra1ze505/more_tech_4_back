from src.data.repos.user import UserRepo


class UserService:

    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def get_all(self):
        return await self.user_repo.get_all()
