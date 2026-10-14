from django.contrib.auth import get_user_model
from django.db import transaction


User = get_user_model()


class UserService:
    def register_user(self, username: str, email: str, password: str, url: str) -> User:
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=True
            )

        return user
