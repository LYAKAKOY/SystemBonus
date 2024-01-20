import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter

from api.handlers.users.handlers import user_router
from api.handlers.auth.handlers import auth_router

app = FastAPI(title="SystemBonus")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(main_api_router)
