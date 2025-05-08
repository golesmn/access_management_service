from sqlalchemy import Boolean, Column, Integer, String

from access_management.domain.aggregates.user import User
from shared.infrastructure.db.db import Base


class UserModel(Base):
    __tablename__ = "users"  # Matches Django’s table name
    __table_args__ = {"extend_existing": True}  # Avoid redefinition errors
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    def to_entity(self):
        return User(username=self.username, email=self.email)

    @staticmethod
    def from_entity(user: User):
        return UserModel(
            username=user.username,
            email=user.email.value,
            hashed_password=user.password,
            is_active=True,
        )
