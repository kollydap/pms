from pydantic import BaseModel, EmailStr, constr, conlist, Field
from enum import Enum
from uuid import UUID
from typing import Optional
from datetime import datetime


class AccountType(str, Enum):
    CREDIT = "CREDIT"
    NON_CREDIT = "NON_CREDIT"


class User(BaseModel):
    first_name: constr(min_length=1)
    last_name: constr(min_length=1)
    phone_number: str
    email: EmailStr


class UserUpdate(BaseModel):
    first_name: constr(min_length=1)
    last_name: constr(min_length=1)
    phone_number: str


class UserProfile(User):
    auth_user_uid: UUID
    user_uid: UUID
    account_type: AccountType
    profile_picture_uid: Optional[UUID]
    timestamp_gmt: datetime


class PaginatedUserProfile(BaseModel):
    match_size: int = 0
    result_size: int = 0
    result_set: conlist(item_type=UserProfile) = []


class UserQuery(BaseModel):
    limit: Optional[int] = Field(None, gt=0, le=50)
    offset: Optional[int] = Field(None, ge=0)
    search_str: Optional[constr(min_length=1)]


class AccountChangeRequest(BaseModel):
    document_uids: Optional[conlist(item_type=UUID)]


class AccountChangeRequestProfile(AccountChangeRequest):
    user_uid: UUID
    account_change_request_uid: UUID
