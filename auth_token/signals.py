from django.contrib.auth.signals import user_logged_in

from auth_token.models import AuthenticationToken


def generate_keys_after_logged_in(sender, user, request, **kwargs):
    authentication_token, created = AuthenticationToken.objects.get_or_create(user=user)
    if not created:
        if not authentication_token.is_active:
            authentication_token.get_random()
            authentication_token.save()


user_logged_in.connect(generate_keys_after_logged_in)
