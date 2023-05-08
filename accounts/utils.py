import binascii
import os

import shopify
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from shopify.utils import shop_url

User = get_user_model()


def get_sanitized_shop_param(request):
    sanitized_shop_domain = shop_url.sanitize_shop_domain(
        request.GET.get("shop", request.POST.get("shop"))
    )
    if not sanitized_shop_domain:
        raise ValueError("Shop must match 'example.myshopify.com'")
    return sanitized_shop_domain


def build_auth_params(request):
    scopes = get_configured_scopes()
    redirect_uri = build_redirect_uri()
    state = build_state_param()

    return scopes, redirect_uri, state


def get_configured_scopes():
    return getattr(settings, "SHOPIFY_API_SCOPES").split(",")


def build_redirect_uri():
    app_url = getattr(settings, "APP_URL")
    callback_path = reverse("callback")
    return "https://{app_url}{callback_path}".format(
        app_url=app_url, callback_path=callback_path
    )


def build_state_param():
    return binascii.b2a_hex(os.urandom(15)).decode("utf-8")


def store_state_param(request, state):
    request.session["shopify_oauth_state_param"] = state


def _new_session(shop_url):
    shopify_api_version = getattr(settings, "SHOPIFY_API_VERSION")
    shopify_api_key = getattr(settings, "SHOPIFY_API_KEY")
    shopify_api_secret = getattr(settings, "SHOPIFY_API_SECRET")

    shopify.Session.setup(api_key=shopify_api_key, secret=shopify_api_secret)
    return shopify.Session(shop_url, shopify_api_version)


# Callback helper methods


def validate_params(request, params):
    validate_state_param(request, params.get("state"))
    if not shopify.Session.validate_params(params):  # Validates HMAC
        raise ValueError("Invalid callback parameters")


def validate_state_param(request, state):
    if request.session.get("shopify_oauth_state_param") != state:
        raise ValueError("Anti-forgery state parameter does not match")

    request.session.pop("shopify_oauth_state_param", None)


def exchange_code_for_access_token(request, shop):
    session = _new_session(shop)
    access_token = session.request_token(request.GET)
    access_scopes = session.access_scopes

    return access_token, access_scopes


def store_shop_information(access_token, access_scopes, shop, host):
    user, created = User.objects.get_or_create(shopify_domain=shop)
    user.token = access_token
    user.access_scopes = access_scopes
    user.host = host
    user.save()
    return user


def build_callback_redirect_uri(request, params):
    base = request.session.get("return_to", reverse("root_path"))
    return "{base}?shop={shop}".format(base=base, shop=params.get("shop"))


# callback after_authenticate_jobs helper methods


def after_authenticate_jobs(shop, access_token):
    create_uninstall_webhook(shop, access_token)


def create_uninstall_webhook(shop, access_token):
    with shopify_session(shop, access_token):
        app_url = getattr(settings, "APP_URL")
        webhook = shopify.Webhook()
        webhook.topic = "app/uninstalled"
        webhook.address = "https://{host}/uninstall".format(host=app_url)
        webhook.format = "json"
        webhook.save()


def shopify_session(shopify_domain, access_token):
    api_version = getattr(settings, "SHOPIFY_API_VERSION")

    return shopify.Session.temp(shopify_domain, api_version, access_token)


def get_backend():
    backend = (
        getattr(settings, "SHOPIFY_BACKEND")
        if hasattr(settings, "SHOPIFY_BACKEND")
        else None
    )
    return backend
