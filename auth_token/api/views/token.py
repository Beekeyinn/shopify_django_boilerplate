from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from auth_token.api.serializers import AuthenticationTokenSerializers
from auth_token.models import AuthenticationToken

from rest_framework.permissions import IsAuthenticated


class AuthenticationRetrieveViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = AuthenticationTokenSerializers
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return AuthenticationToken.objects.filter(user=self.request.user)
