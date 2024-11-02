from typing import Protocol

from models import User
from services.user.user_service import UserService


class UserServiceProtocol(Protocol):
    async def get_user(self, user_id: int) -> User | None:
        ...
