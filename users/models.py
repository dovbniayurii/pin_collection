from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, useremail, password=None):
        if not useremail:
            raise ValueError(_('The Useremail field must be set'))
        user = self.model(useremail=self.normalize_email(useremail))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, useremail, password=None):
        user = self.create_user(useremail, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    useremail = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'useremail'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.useremail

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
