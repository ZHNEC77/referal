from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import endpoints as auth_endpoints
from app.api.referral import endpoints as referral_endpoints


load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_endpoints.router, prefix="/api/auth", tags=["auth"])
app.include_router(referral_endpoints.router,
                   prefix="/api/referral", tags=["referral"])
