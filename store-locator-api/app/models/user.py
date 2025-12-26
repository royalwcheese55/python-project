from sqlalchemy import Column, String, Enum
from app.db.database import Base

RoleEnum = Enum("admin", "marketer", "viewer", name="role_enum")
UserStatusEnum = Enum("active", "inactive", name="user_status_enum")

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)  # e.g. U001
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(RoleEnum, nullable=False)
    status = Column(UserStatusEnum, nullable=False, default="active")