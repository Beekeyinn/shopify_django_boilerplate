from accounts.models import User
from django.conf import settings


def get_shopify_context(request):
    if isinstance(request.user, User):
        return {
            "shop_auth":True,
            "shopify": {
                "shopify_domain": request.user.shopify_domain,
                "domain_prefix": str(request.user.shopify_domain).split(
                    ".", maxsplit=2
                )[0],
                "host": request.user.host,
                "app_id": getattr(settings, "SHOPIFY_API_KEY"),
            }
        }
    else:
        return {
            "shopify": {
                "shopify_domain": request.GET.get("shop",None),
                "domain_prefix": str(request.GET.get("shop",None)).split(
                    ".", maxsplit=2
                )[0],
                "host": request.GET.get("host",None),
                "app_key": getattr(settings, "SHOPIFY_API_KEY"),
            }
        }
