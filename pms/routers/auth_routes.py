from fastapi import APIRouter, status, Body, Depends
from pms.models.user_models import (
    TokenProfile,
    UserSignUp,
    AuthenticatedUserProfile,
    Login,
    PasswordChange,
    TokenVerification,
)
from typing import Annotated
from pydantic import EmailStr
import pms.service.user_service as user_service
from pms.routers.routes_utils import get_refresh_token


from fastapi import Depends

AnEmail = Annotated[EmailStr, Body(embed=True)]
AnToken = Annotated[str, Body(embed=True)]
AnRefreshToken = Annotated[str, Depends(get_refresh_token)]


api_router = APIRouter(tags=["Authentication"], prefix="/api/v1/accounts")


@api_router.post("/signup", response_model=TokenProfile)
async def user_signup(user_signup: UserSignUp):
    return await user_service.user_signup(user_signup=user_signup)


@api_router.post("/login", response_model=AuthenticatedUserProfile)
async def login_user(login: Login):
    return await user_service.login_user(login=login)


@api_router.post("/forgot/password", response_model=TokenProfile)
async def forgot_password(email: AnEmail):
    return await user_service.forgot_password(email=email)


@api_router.post("/change/password")
async def change_password(password_change: PasswordChange):
    return await user_service.change_password(password_change=password_change)


@api_router.post("/token/verification")
async def token_verification(token_verification: TokenVerification):
    print('heeee')
    return await user_service.token_verification(token_verification=token_verification)


@api_router.post("/logout")
async def logout():
    return await user_service.logout()


# Todo Create a background TAsk to create user profile


@api_router.get("/refresh", response_model=AuthenticatedUserProfile)
async def refresh(refresh_token: AnRefreshToken):
    return await user_service.refresh(refresh_token=refresh_token)
