from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import User
from auth_token.models import AuthenticationToken
from django.core.exceptions import PermissionDenied


def home_redirect_view_decorator(func):
    def wrapper(*args, **kwargs):
        request = args[1]

        if (
            request.GET.get("auth", None) is not None
            and request.GET.get("sh", None) is not None
        ):
            try:
                user = User.objects.get(shopify_domain=request.GET.get("sh", None))
                auth = AuthenticationToken.objects.get(
                    auth_token=request.GET.get("auth", None)
                )
                if user != auth.user:
                    raise PermissionDenied()
                else:
                    kwargs["auth"] = auth
                    kwargs["shopify_domain"] = request.GET.get("sh", None)
                    kwargs["token"] = request.GET.get("auth", None)
                    return func(*args, **kwargs)
            except (
                User.DoesNotExist,
                AuthenticationToken.DoesNotExist,
                PermissionDenied,
            ) as exc:
                print("Exception occured", exc)
                return redirect(reverse("login"))

        return redirect(reverse("login"))

    return wrapper
