from typing import Optional

from sqlalchemy.orm import Session

from access_management.infrastructure.models import UserModel
from shared.infrastructure.db.sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[UserModel]):
    def __init__(self, session: Session):
        super().__init__(session, UserModel)

    def find_by_email(self, email: str) -> Optional[UserModel]:
        return self.session.query(UserModel).filter_by(email=email).first()
