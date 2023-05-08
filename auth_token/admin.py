from django.contrib import admin

# Register your models here.
from .models import AuthenticationToken

admin.site.register(AuthenticationToken)