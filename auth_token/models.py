from typing import Iterable, Optional
from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from base.models import ExtraFieldsModelsMixin

# Create your models here.
from .utils import get_random_string_and_numbers, generate_random_token


class AuthenticationToken(ExtraFieldsModelsMixin, models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="auth_token")
    auth_token = models.CharField(
        verbose_name=_("Stand Alone Authentication Token"), max_length=100, unique=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Valid"),
        error_messages={False: "The provided token is not valid"},
    )

    def __str__(self) -> str:
        return f"{self.user.shopify_domain}->{self.auth_token}"

    def get_random(self):
        if not self.is_active:
            self.auth_token = get_random_string_and_numbers(size=70)

    def save(self, *args, **kwargs) -> None:
        if not self.auth_token or self.auth_token is None or not self.is_active:
            self.auth_token = generate_random_token(self, size=70)
            self.is_active = True if not self.is_active else True
        return super().save(*args, **kwargs)
