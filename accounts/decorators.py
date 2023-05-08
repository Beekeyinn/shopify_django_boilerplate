from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from shopify import ApiAccess, Session, session_token
from accounts.models import User
from accounts.utils import get_sanitized_shop_param

HTTP_AUTHORIZATION_HEADER = "HTTP_AUTHORIZATION"


def session_token_required(func):
    def wrapper(*args, **kwargs):
        try:
            decoded_session_token = session_token.decode_from_header(
                authorization_header=authorization_header(args[0]),
                api_key=getattr(settings, "SHOPIFY_API_KEY"),
                secret=getattr(settings, "SHOPIFY_API_SECRET"),
            )
            with shopify_session(decoded_session_token, args[0]):
                return func(*args, **kwargs)
        except session_token.SessionTokenError:
            return HttpResponse(status=401)

    return wrapper


def shopify_session(session_token, request):
    shopify_domain = session_token.get("dest").removeprefix("https://")
    request.shopify_domain = shopify_domain
    api_version = getattr(settings, "SHOPIFY_API_VERSION")
    access_token = User.objects.get(shopify_domain=shopify_domain).token
    request.access_token = access_token
    request.api_version = api_version
    return Session.temp(shopify_domain, api_version, access_token)


def authorization_header(request):
    return request.META.get(HTTP_AUTHORIZATION_HEADER)


def known_shop_required(func):
    def wrapper(*args, **kwargs):
        request = args[1]
        if isinstance(request.user, User):
            return func(*args, **kwargs)
        try:
            check_shop_domain(request, kwargs)
            check_shop_known(request, kwargs)

            return func(*args, **kwargs)
        except Exception as e:
            return redirect(reverse("login"))

    return wrapper


def check_shop_domain(request, kwargs):
    kwargs["shopify_domain"] = get_sanitized_shop_param(request)


def check_shop_known(request, kwargs):
    kwargs["shop"] = User.objects.get(shopify_domain=kwargs.get("shopify_domain"))


def latest_access_scopes_required(func):
    def wrapper(*args, **kwargs):
        shop = kwargs.get("shop")
        request = args[1]
        if isinstance(request.user, User):
            return func(*args, **kwargs)
        try:
            configured_access_scopes = getattr(settings, "SHOPIFY_API_VERSION")
            current_access_scopes = getattr(settings, "SHOPIFY_API_SCOPES")

            assert ApiAccess(configured_access_scopes) == ApiAccess(
                current_access_scopes
            )
        except:
            kwargs["scope_changes_required"] = True

        return func(*args, **kwargs)

    return wrapper
