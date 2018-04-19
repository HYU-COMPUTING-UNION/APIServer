from django.db import models
from django.contrib.auth.models import AbstractUser


class AffiliationAuth(models.Model):
    """Student data related to authentication of affiliation"""
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Profile model"""
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=255)
    is_affiliation_authenticated = models.BooleanField(default=False)

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
    def is_affiliation_authenticated(self):
        return (self.profile is not None
                and self.profile.is_affiliation_authenticated)
