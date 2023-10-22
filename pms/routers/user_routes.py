from fastapi import APIRouter, Body
from pms.models.user_models import (
    AccountChangeRequest,
    UserProfile,
    UserUpdate,
    AccountChangeRequestProfile,
)
from typing import Annotated
import pms.service.user_service as user_service
from uuid import UUID


AnProfilePicture = Annotated[UUID, Body(embed=True)]
api_router = APIRouter(tags=["user"], prefix="/api/v1/profile")



@api_router.get(
    "",
    response_model=UserProfile,
)
async def get_user_profile():
    return await user_service.get_user_profile()


@api_router.patch(
    "",
    response_model=UserProfile,
)
async def update_user_profile(user_update: UserUpdate):
    return await user_service.update_user_profile(user_update=user_update,x_user_uid=1)


@api_router.patch(
    "/picture",
    response_model=UserProfile,
)
async def update_user_profile_picture(profile_picture_uid: AnProfilePicture):
    return await user_service.update_user_picture(
        profile_picture_uid=profile_picture_uid
    )


@api_router.delete(
    "/picture",
    response_model=UserProfile,
)
async def remove_user_picture():
    return await user_service.remove_user_picture()


@api_router.post(
    "/type/change",
    response_model=AccountChangeRequestProfile,
)
async def request_user_account_type_change(
    account_change_request: AccountChangeRequest,
):
    return await user_service.request_user_account_type_change(
        account_change_request=account_change_request
    )
