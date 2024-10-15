from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Referral, User
from app.api.referral.schemas import ReferralCreate
import uuid


class ReferralService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_referral(self, user_id: int, expiration_date: date):
        referral_code = str(uuid.uuid4())
        db_referral = Referral(referral_code=referral_code,
                               expiration_date=expiration_date, referrer_id=user_id)
        self.db.add(db_referral)
        await self.db.commit()
        await self.db.refresh(db_referral)
        return referral_code

    async def delete_referral(self, user_id: int):
        query = select(Referral).filter(Referral.referrer_id == user_id)
        result = await self.db.execute(query)
        referral = result.scalars().first()
        if referral:
            await self.db.delete(referral)
            await self.db.commit()

    async def get_referral_by_user_id(self, user_id: int):
        query = select(Referral).filter(Referral.referrer_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_referral_by_email(self, email: str):
        query = select(Referral).join(
            Referral.referrer).filter(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_referrer_by_code(self, referral_code: str):
        query = select(Referral).filter(
            Referral.referral_code == referral_code)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def add_referral(self, referrer_id: int, referral_id: int):
        pass  # Implement this if needed

    async def get_referrals_by_referrer_id(self, referrer_id: int):
        query = select(Referral).filter(Referral.referrer_id == referrer_id)
        result = await self.db.execute(query)
        return result.scalars().all()
