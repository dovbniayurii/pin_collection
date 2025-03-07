from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets
from .models import PinUser,OTP,FCMToken
User = get_user_model()

# Unregister the default User model
admin.site.register(FCMToken)

# Register your custom User model
@admin.register(PinUser)
class UserAdmin(admin.ModelAdmin):
    pass

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]