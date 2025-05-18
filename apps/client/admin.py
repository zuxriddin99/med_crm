from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'workplace')
    list_filter = ('workplace',)
    search_fields = ('first_name', 'last_name', 'phone_number', 'address', 'workplace')
    ordering = ('-id',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Shaxsiy ma’lumotlar', {
            'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth')
        }),
        ('Qo‘shimcha ma’lumotlar', {
            'fields': ('address', 'workplace', 'description')
        }),
    )
