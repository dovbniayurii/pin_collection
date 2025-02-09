from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets

User = get_user_model()

# Unregister the default User model
admin.site.unregister(User)

# Register your custom User model
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]