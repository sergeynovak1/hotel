from django.contrib.auth.models import UserManager as DjangoUserManager, User
from typing import Optional


class UserManager(DjangoUserManager):
    def _create_user(self, email: str, password: str, commit: bool = True, **extra_fields) -> User:
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_user(self, email: str, password: Optional[str] = None, **extra_fields) -> User:
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields) -> User:
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
