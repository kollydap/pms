from pms.models.user_models import UserUpdate, AccountChangeRequest, User
import pms.database.db_handlers.user_db_handler as user_db_handler
import logging
from pms.service.service_exceptions import NotFoundError, DuplicateError, UpdateError
from pms.service.service_errors import PmsErrorEnum
from uuid import UUID
from errors.k_api_error import KApiError

LOGGER = logging.getLogger(__file__)


async def get_user_profile(x_user_uid: UUID, **kwargs):
    try:
        return await user_db_handler.get_user_profile(x_user_uid=x_user_uid)
    except NotFoundError as e:
        LOGGER.exception(e)
        raise KApiError(PmsErrorEnum.PMS_005)


async def update_user_profile(user_update: UserUpdate, x_user_uid, **kwargs):
    try:
        return await user_db_handler.update_user_profile(
            user_update=user_update, x_user_uid=x_user_uid
        )
    except UpdateError as e:
        LOGGER.exception(e)
        raise KApiError(PmsErrorEnum.PMS_002)


async def update_user_picture(profile_picture_uid: UUID, x_user_uid: UUID, **kwargs):
    try:
        return await user_db_handler.update_user_picture(
            profile_picture_uid=profile_picture_uid, x_user_uid=x_user_uid
        )
    except UpdateError as e:
        LOGGER.exception(e)
        raise KApiError(PmsErrorEnum.PMS_002)


async def remove_user_picture(x_user_uid: UUID, **kwargs):
    try:
        return await user_db_handler.update_user_picture(
            profile_picture_uid=None, x_user_uid=x_user_uid
        )
    except NotFoundError as e:
        LOGGER.exception(e)
        raise KApiError(PmsErrorEnum.PMS_005)


async def request_user_account_type_change(
    account_change_request: AccountChangeRequest, x_user_uid: UUID, **kwargs
):
    try:
        return await user_db_handler.request_user_account_type_change(
            account_change_request=account_change_request, x_user_uid=x_user_uid
        )
    except DuplicateError as e:
        LOGGER.exception(e)
        raise KApiError(
            PmsErrorEnum.PMS_002,
            extra_detail="You have already requested account change",
        )


# ========================== listener functions=========================================#


async def user_profile_creation_listener(user: User, user_uid: int):
    await user_db_handler.create_user(user=user, x_user_uid=user_uid)


async def user_profile_deletion_listener(user_uid: int):
    await user_db_handler.delete_user_profile(x_user_uid=user_uid)
