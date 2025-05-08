import json
import logging

from flask import request
from kafka import KafkaProducer

from access_management.application.services.user_service import UserService
from access_management.domain.aggregates.user import User
from access_management.repositories.user_repository import UserRepository
from shared.infrastructure.db.db import SessionLocal
from shared.infrastructure.db.uow import UnitOfWork
from shared.infrastructure.messaging.kafka_producer import KafkaEventDispatcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_message_kafka(bootstrap_servers: str, topic: str, message: dict):
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

        producer.send(topic, message)
        producer.flush()
        logger.info(f"Message sent to topic '{topic}' successfully.")
    except Exception as e:
        logger.error(f"Failed to send message to Kafka: {e}")


kafka_dispatcher = KafkaEventDispatcher(
    "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"
)


def main():
    user_payload = request.get_json()
    uow = UnitOfWork(SessionLocal, kafka_dispatcher)

    user_repo = UserRepository(uow.session)
    user_service = UserService(user_repo=user_repo)
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
