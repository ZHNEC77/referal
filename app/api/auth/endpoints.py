from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.services.referral_service import ReferralService
from app.services.user_service import UserService
from app.api.auth.schemas import UserCreate, Token

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db=Depends(get_db)):
    auth_service = AuthService(db)
    user_service = UserService(db)
    existing_user = await user_service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = await auth_service.register_user(user)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register_with_referral", response_model=Token)
async def register_with_referral(user: UserCreate, referral_code: str, db=Depends(get_db)):
    auth_service = AuthService(db)
    user_service = UserService(db)
    referral_service = ReferralService(db)
    existing_user = await user_service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    referrer = await referral_service.get_referrer_by_code(referral_code)
    if not referrer:
        raise HTTPException(status_code=400, detail="Invalid referral code")
    user_id = await auth_service.register_user(user)
    await referral_service.add_referral(referrer.id, user_id)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
