from django.urls import include, path
from rest_framework.routers import DefaultRouter

from auth_token.api.views import AuthenticationRetrieveViewSet

router = DefaultRouter()
router.register("", AuthenticationRetrieveViewSet, basename="authentication")

urlpatterns = [
    path("", include(router.urls)),
]
