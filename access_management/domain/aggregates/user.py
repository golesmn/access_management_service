from dataclasses import asdict
from datetime import datetime
from uuid import uuid4

from access_management.domain.events.user_created import UserCreated
from access_management.domain.value_objects.email import Email
from shared.abstractions.primitives.aggregate import AggregateRoot


class User(AggregateRoot):
    def __init__(self, username, email, password):
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        self.is_active: bool = True

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

    def _generate_id(self) -> str:
        import uuid

        return str(uuid.uuid4())

    def deactivate(self):
        self.is_active = False

    @classmethod
    def create(cls, username: str, email: str, password: str):
        user = cls(username=username, email=Email(email), password=password)
        user.add_event(
            event=UserCreated(
                email=email,
                user_id=uuid4(),
                event_id=uuid4(),
                event_type="test",
                timestamp=datetime.now(),
            )
        )
        return user
