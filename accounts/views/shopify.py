import json
from pprint import pprint

from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from accounts.authentication import authenticate
from accounts.models import User
from accounts.utils import (
    after_authenticate_jobs,
    build_callback_redirect_uri,
    exchange_code_for_access_token,
    get_backend,
    store_shop_information,
    validate_params,
)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        pprint(request.GET.__dict__)
        if request.GET.get("shop"):
            return authenticate(request)
        return render(request, "login.html", {"app_name": "Sample Django app"})

    def post(self, request):
        return authenticate(request)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        auth_token = request.user.auth_token
        auth_token.is_active = False
        auth_token.save()
        logout(request)
        return redirect(reverse("login"))


def callback(request):
    params = request.GET.dict()
    shop = params.get("shop")
    host = params.get("host")

    try:
        validate_params(request, params)
        access_token, access_scopes = exchange_code_for_access_token(request, shop)
        user = store_shop_information(access_token, access_scopes, shop, host)
        login(request, user, backend=get_backend())
        after_authenticate_jobs(shop, access_token)
    except ValueError as exception:
        messages.error(request, str(exception))
        return redirect(reverse("login"))

    redirect_uri = build_callback_redirect_uri(request, params)
    return redirect(redirect_uri)


@csrf_exempt
def uninstall(request):
    uninstall_data = json.loads(request.body)
    shop = uninstall_data.get("domain")
    User.objects.filter(shopify_domain=shop).delete()
    return HttpResponse(status=204)
