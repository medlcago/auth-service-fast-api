import sqlalchemy as sa
from sqlalchemy import or_

from core.repository import BaseRepository
from models import User
from schemas.auth import SignUpSchema


class UserRepository(BaseRepository[User, SignUpSchema]):
    model_type = User

    async def get_by_username_or_email(self, username: str, email: str) -> User | None:
        stmt = sa.select(self.model_type).where(
            or_(self.model_type.username.ilike(username), self.model_type.email.ilike(email))
        )
        return await self.session.scalar(stmt)
