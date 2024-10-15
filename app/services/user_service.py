from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str):
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()
