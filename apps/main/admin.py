from django.contrib import admin

from apps.main.models import ClinicBranch


# Register your models here.
@admin.register(ClinicBranch)
class ClinicBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address')
    search_fields = ('name', 'address')
