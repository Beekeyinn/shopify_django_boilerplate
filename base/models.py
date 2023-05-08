from django.db import models
from uuid import uuid4


class ExtraFieldsModelsMixin(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
