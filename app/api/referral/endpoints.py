from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.db.session import get_db
from app.services.referral_service import ReferralService
from app.api.referral.schemas import ReferralCreate, Referral

router = APIRouter()


@router.post("/create", response_model=Referral)
async def create_referral(referral: ReferralCreate, current_user=Depends(get_current_user), db=Depends(get_db)):
    referral_service = ReferralService(db)
    existing_referral = await referral_service.get_referral_by_user_id(current_user.id)
    if existing_referral:
        raise HTTPException(
            status_code=400, detail="Referral code already exists")
    referral_code = await referral_service.create_referral(current_user.id, referral.expiration_date)
    return {"referral_code": referral_code, "expiration_date": referral.expiration_date}


@router.delete("/delete")
async def delete_referral(current_user=Depends(get_current_user), db=Depends(get_db)):
    referral_service = ReferralService(db)
    await referral_service.delete_referral(current_user.id)
    return {"detail": "Referral code deleted"}


@router.get("/get_by_email", response_model=Referral)
async def get_referral_by_email(email: str, db=Depends(get_db)):
    referral_service = ReferralService(db)
    referral = await referral_service.get_referral_by_email(email)
    if not referral:
        raise HTTPException(status_code=404, detail="Referral code not found")
    return referral


@router.get("/get_referrals/{referrer_id}", response_model=list[Referral])
async def get_referrals(referrer_id: int, db=Depends(get_db)):
    referral_service = ReferralService(db)
    referrals = await referral_service.get_referrals_by_referrer_id(referrer_id)
    return referrals
