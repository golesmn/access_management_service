from werkzeug.security import generate_password_hash

from access_management.domain.aggregates.user import User
from access_management.infrastructure.models import UserModel
from access_management.infrastructure.repositories.user_repository import UserRepository
from shared.infrastructure.db.db import SessionLocal


def create_user(user: User) -> User:
    hashed_password = generate_password_hash(user.password)
    db_user = UserModel(
        username=user.username,
        email=user.email.value,
        hashed_password=hashed_password,
        is_active=True,
    )
    db = SessionLocal()
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    finally:
        db.close()
    return user


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user_dto: User) -> User:
        user = UserModel.from_entity(user_dto)
        self.user_repo.save(user)
