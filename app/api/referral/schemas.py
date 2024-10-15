from pydantic import BaseModel
from datetime import date


class ReferralCreate(BaseModel):
    expiration_date: date


class Referral(BaseModel):
    referral_code: str
    expiration_date: date
