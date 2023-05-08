from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model

User = get_user_model()


class ShopifyAuthenticationBackend(ModelBackend):
    def authenticate(
        self, request, username=None, password=None, *args, **kwargs
    ) -> AbstractBaseUser | None:
        if username is None:
            return None

        try:
            user = User._default_manager.get_by_natural_key(username)
        except User.DoesNotExist:
            User().set_password()
        else:
            if self.user_can_authenticate(user):
                return user
