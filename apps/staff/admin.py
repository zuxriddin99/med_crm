# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.staff.models import StaffUser


@admin.register(StaffUser)
class StaffUserAdmin(UserAdmin):
    model = StaffUser
    list_display = ('username', 'role', 'branch', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('role', 'branch', 'is_active', 'is_superuser')
    search_fields = ('username', 'branch__name')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ()}),
        (_('Clinic Info'), {'fields': ('role', 'branch')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'branch', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
