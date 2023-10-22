import databases
from pms.models.user_models import AccountType
from sqlalchemy import Column, Integer, String, Enum
import sqlalchemy


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
database = databases.Database(SQLALCHEMY_DATABASE_URL)


metadata = sqlalchemy.MetaData()

User = sqlalchemy.Table(
    "user",
    metadata,
    Column("user_uid", Integer, primary_key=True),
    Column("first_name", String, index=True, nullable=True),
    Column("last_name", String, index=True, nullable=True),
    Column("auth_user_uid", Integer, index=True, nullable=False),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("phone_number", String, nullable=False, unique=False, index=True),
    Column("profile_picture_uid", Integer, nullable=True),
    Column(
        "account_type",
        Enum(AccountType),
        nullable=True,
        default=AccountType.NON_CREDIT,
    ),
)

engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
