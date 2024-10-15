from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    referrals = relationship("Referral", back_populates="referrer")


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    referral_code = Column(String, unique=True, index=True)
    expiration_date = Column(DateTime)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referrer = relationship("User", back_populates="referrals")
