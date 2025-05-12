import logging

from flask import request

from access_management.application.services.user_service import UserService
from access_management.domain.aggregates.user import User
from access_management.infrastructure.repositories.user_repository import UserRepository
from shared.utils.create_service import create_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    user_payload = request.get_json()
    user_service, uow = create_service(UserRepository, UserService)
    user = User.create(**user_payload)
    user_service.create_user(user_dto=user)
    uow.register(user)
    uow.commit()
    return {"message": "User Created Successfully"}


def consumer():
    body = request.get_json()
    method = request.method
    route = request.root_url

    logger.info(f"{body} {method} {route}")
    return {"status": 200, "body": body}
