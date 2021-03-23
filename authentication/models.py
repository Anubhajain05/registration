import uuid

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, uid, email, password=None):

        if email is None:
            raise TypeError('User should have a email')


        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.uid = uid
        user.save()

        return user

    def create_superuser(self, uid, email, password=None):

        if password is None:
            raise TypeError('password should not be none')

        user = self.create_user(uid, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user



class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False)

    USERNAME_FIELD = 'email'


    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access': str(refresh.access_token)

        }


class VerifyEmail(models.Model):
    objects = None
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable= False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verify_users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table="verify-emails"




# Create your models here.
