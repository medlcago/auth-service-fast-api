from core.uow import IUnitOfWork
from models import User


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_user(self, user_id: int) -> User | None:
        async with self.uow:
            return await self.uow.user_repository.get(user_id)
