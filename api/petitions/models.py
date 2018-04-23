from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=50)
    parent = models.ForeignKey(
        'self',
        related_name='sub_categories',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Petition(models.Model):
    class Meta:
        ordering = ['-issued_at']

    issuer = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='issued_petitions',
    )
    assentients = models.ManyToManyField(
        'accounts.Profile',
        related_name='assentient_petitions',
        blank=True,
    )
    categories = models.ManyToManyField(
        Category,
        related_name='petitions',
        blank=True,
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    issued_at = models.DateField(auto_now_add=True)
    expired_at = models.DateField(blank=True)
    is_in_progress = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        expiration_period = getattr(
            settings, 'PETITION_EXPIRATION_PERIOD', timedelta(days=30),
        )

        if self.expired_at is None:
            self.expired_at = timezone.now().date() + expiration_period

        super().save(*args, **kwargs)

    @property
    def assentient_count(self):
        return self.assentients.count()

    @property
    def is_expired(self):
        return timezone.now().date() > self.expired_at

    @property
    def is_answered(self):
        return self.answer is not None


class Answer(models.Model):
    petition = models.OneToOneField(
        Petition,
        on_delete=models.CASCADE,
        related_name='answer',
    )
    content = models.TextField()
    answered_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.petition.title
