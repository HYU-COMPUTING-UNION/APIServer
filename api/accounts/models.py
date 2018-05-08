from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(models.Model):
    """Profile model"""
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return '%s' % self.name


class User(AbstractUser):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True,
    )

    @property
    def is_email_authenticated(self):
        try:
            return self.email_auth.is_email_authenticated
        except EmailAuth.DoesNotExist:
            return False


class EmailAuth(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='email_auth',
        primary_key=True,
    )
    token = models.CharField(max_length=255, unique=True)
    is_email_authenticated = models.BooleanField(default=False)
