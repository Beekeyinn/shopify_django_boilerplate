from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt

from accounts.decorators import known_shop_required, latest_access_scopes_required
from django.contrib.auth import login, authenticate
from django.conf import settings
from accounts.models import User
from django.contrib.auth.models import AnonymousUser
from home.decorator import home_redirect_view_decorator


class HomeView(View):
    @xframe_options_exempt
    @known_shop_required
    @latest_access_scopes_required
    def get(self, request, *args, **kwargs):
        if (
            not isinstance(request.user, User)
            and isinstance(request.user, AnonymousUser)
            and request.GET.get("hmac", None) is not None
            and request.GET.get("host", None) is not None
            and request.GET.get("timestamp", None) is not None
        ):
            try:
                user = authenticate(request, username=kwargs.get("shopify_domain"))
                login(request, user)
            except Exception as e:
                print("HOME EXCEPTION", e)
                return redirect(reverse("login"))
            context = {
                "shop_origin": user.shopify_domain,
                "api_key": getattr(settings, "SHOPIFY_API_KEY"),
                "scope_changes_required": user.access_scopes,
            }
            return render(request, "index.html")
        context = {
            "shop_origin": kwargs.get("shopify_domain"),
            "api_key": getattr(settings, "SHOPIFY_API_KEY"),
            "scope_changes_required": kwargs.get("scope_changes_required"),
        }
        return render(request, "index.html", context)


class RedirectHomeView(View):
    @home_redirect_view_decorator
    def get(self, request, *args, **kwargs):
        try:
            user = authenticate(request, username=kwargs.get("shopify_domain"))
            login(request, user)
        except Exception as e:
            print("HOME EXCEPTION", e)
            return redirect(reverse("login"))
        else:
            return redirect(reverse("root_path"))
