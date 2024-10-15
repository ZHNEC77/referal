from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import get_password_hash, verify_password
from app.db.models import User
from app.api.auth.schemas import UserCreate
import logging

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, user: UserCreate):
        try:
            # Проверка на существование пользователя с таким же email
            existing_user = await self.get_user_by_email(user.email)
            if existing_user:
                logger.warning(f"User with email {user.email} already exists.")
                return None

            hashed_password = get_password_hash(user.password)
            db_user = User(email=user.email, hashed_password=hashed_password)
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            logger.info(
                f"User with email {user.email} registered successfully.")
            return db_user.id
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            await self.db.rollback()
            raise

    async def authenticate_user(self, email: str, password: str):
        try:
            user = await self.get_user_by_email(email)
            if not user:
                logger.warning(f"User with email {email} not found.")
                return None
            if not verify_password(password, user.hashed_password):
                logger.warning(
                    f"Incorrect password for user with email {email}.")
                return None
            logger.info(f"User with email {email} authenticated successfully.")
            return user
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            await self.db.rollback()
            raise

    async def get_user_by_email(self, email: str):
        try:
            query = select(User).where(User.email == email)
            result = await self.db.execute(query)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            await self.db.rollback()
            raise
