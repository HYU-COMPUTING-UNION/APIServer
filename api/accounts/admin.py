from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import AffiliationAuth, User, Profile


@admin.register(AffiliationAuth)
class AffiliationAuthAdmin(admin.ModelAdmin):
    search_fields = ['name', 'student_id']
    list_display = ['name', 'student_id']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['name', 'student_id']
    list_display = ['name', 'student_id', 'is_affiliation_authenticated',
                    'associate_users']
    list_filter = ['is_affiliation_authenticated']

    def associate_users(self, obj):
        return obj.users.count()


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fieldsets = list(self.fieldsets)
        fieldsets.insert(1,
            ('Profile', {'fields': ['profile']}),   # noqa
        )
        self.fieldsets = fieldsets
