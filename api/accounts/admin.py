from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import User, Profile, EmailAuth


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['name', 'student_id']
    list_display = [
        'name',
        'email',
        'associate_users',
    ]

    def associate_users(self, obj):
        return obj.users.count()


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fieldsets = list(self.fieldsets)
        fieldsets.insert(
            1,
            ('Profile', {'fields': ['profile']}),
        )
        self.fieldsets = fieldsets


@admin.register(EmailAuth)
class EmailAuthAdmin(admin.ModelAdmin):
    search_fields = ['user__profile__name']
    list_display = ['user_name', 'token', 'is_email_authenticated']

    def user_name(self, obj):
        return obj.user.profile.name
