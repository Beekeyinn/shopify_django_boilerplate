from rest_framework import serializers

from accounts.models import User
from auth_token.api.serializers import AuthenticationTokenSerializers


class UserSerializer(serializers.ModelSerializer):
    authentication = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "is_active",
            "is_admin",
            "authentication",
            "shopify_domain",
            "access_scopes",
            "updated_at",
            "created_at",
            "host",
        )
        read_only_fields = (
            "id",
            "is_active",
            "is_admin",
            "shopify_domain",
            "host",
            "access_scopes",
            "updated_at",
            "created_at",
            "authentication",
        )

    def get_authentication(self, obj):
        return AuthenticationTokenSerializers(obj.auth_token, many=False).data
