from django.urls import path, include

urlpatterns = [
    path("users/", include("accounts.api.urls")),
]
