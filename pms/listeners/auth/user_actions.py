from pms.models.user_models import User
import pms.service.user_service as user_service


async def user_account_create(data_obj: dict):
    auth_user_uid = data_obj["auth_user_uid"]
    if "auth_user_uid" in data_obj:
        del data_obj["auth_user_uid"]

    user = User(**data_obj)
    await user_service.user_profile_creation_listener(user=user, user_uid=auth_user_uid)


async def user_account_deleted(data_object: dict):
    auth_user_uid = data_object["auth_user_uid"]
    await user_service.user_profile_deletion_listener(user_uid=auth_user_uid)
