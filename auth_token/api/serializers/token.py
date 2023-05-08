from rest_framework import serializers
from auth_token.models import AuthenticationToken


class AuthenticationTokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationToken
        fields = (
            "id",
            "user",
            "is_active",
            "auth_token",
            "created_at",
            "deleted_at",
            "updated_at",
            "auth_token",
        )
        read_only_fields = (
            "id",
            "user",
            "is_active",
            "auth_token",
            "created_at",
            "deleted_at",
            "updated_at",
        )
