from accounts.utils import (
    _new_session,
    build_auth_params,
    get_sanitized_shop_param,
    store_state_param,
)
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login
from rest_framework.authentication import SessionAuthentication


def authenticate(request):
    try:
        shop = get_sanitized_shop_param(request)
        scopes, redirect_uri, state = build_auth_params(request)
        store_state_param(request, state)
        permission_url = _new_session(shop).create_permission_url(
            scopes, redirect_uri, state
        )
        return redirect(permission_url)
    except ValueError as exception:
        messages.error(request, str(exception))
        return redirect(reverse("login"))


class CsrfExemptAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
