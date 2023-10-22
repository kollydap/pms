from uuid import UUID
from sqlalchemy import update, insert, select, delete, insert
from pms.database.db_models.user_orm import User as UserDb
from pms.models.user_models import User, UserProfile, UserUpdate
import logging
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, OperationalError

from pms.service.service_exceptions import (
    DuplicateError,
    NotFoundError,
)
from pms.database.db_models.user_orm import database

LOGGER = logging.getLogger(__file__)


async def create_user(user: User, x_user_uid: int, **kwargs):
    user_data = user.dict()
    user_data["auth_user_uid"] = x_user_uid
    query = UserDb.insert().values(**user_data)
    try:
        await database.execute(query)
        new_user_query = UserDb.select().where(UserDb.c.email == user_data["email"])
        new_user = await database.fetch_one(new_user_query)

        return UserProfile(
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            phone_number=new_user.phone_number,
            email=new_user.email,
            auth_user_uid=new_user.auth_user_uid,
            user_uid=new_user.user_uid,
            account_type=new_user.account_type,
            profile_picture_uid=new_user.profile_picture_uid,
        )

    except IntegrityError as e:
        print(f"Error creating user: {e}")
        return False


async def update_user_profile(user_update: UserUpdate, x_user_uid: UUID, **kwargs):
    user_update_dict = user_update.dict(exclude_none=True)
    # query = UserDb.update(


async def delete_user_profile(user_uid: int, **kwargs):
    # Define a SQLAlchemy DELETE statement with the returning clause
    delete_query = (
        delete(UserDb).where(UserDb.auth_user_uid == user_uid).returning(UserDb)
    )

    # Execute the DELETE query and fetch the deleted row
    result = await database.execute(delete_query)

    # Check if any rows were deleted and return the deleted user info
    if not result:
        raise NotFoundError  # Assuming it returns a single row

    return UserProfile(**result.as_dict())  # User not found or already deleted
