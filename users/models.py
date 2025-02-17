from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class PinUserManager(BaseUserManager):
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

class PinUser(AbstractBaseUser):
    useremail = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = PinUserManager()

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


from django.db import models
from django.utils import timezone
import random
import string

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def generate_otp(cls, user):
        otp_value = ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit OTP
        expires_at = timezone.now() + timezone.timedelta(minutes=10)  # OTP expires in 10 minutes
        otp_instance = cls.objects.create(user=user, otp=otp_value, expires_at=expires_at)
        return otp_instance
