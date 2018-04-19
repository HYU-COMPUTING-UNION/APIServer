from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, Petition, Answer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'parent_name']

    def parent_name(self, obj):
        return obj.parent.name if obj.parent is not None else _('None')


@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content', 'issuer_name']
    list_display = [
        'title', 'content', 'issuer_name', 'issued_at',
        'expired_at', 'answered_at', 'is_in_progress',
    ]

    def issuer_name(self, obj):
        return obj.issuer.name

    def answered_at(self, obj):
        return obj.answer.answered_at if obj.answer is not None else None


@admin.register(Answer)
class Answer(admin.ModelAdmin):
    search_fields = ['content']
    list_display = ['petition_title', 'content', 'answered_at']

    def petition_title(self, obj):
        return obj.petition.title
