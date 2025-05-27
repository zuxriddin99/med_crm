from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from apps.service.models import Service, ServiceItem


@admin.register(Service)
class ServiceAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = (
        'tree_actions',
        'indented_title',
        'branch',
        'is_active',
        'is_laboratory_analysis',
        'queue_letter',
    )
    list_display_links = ('indented_title',)
    list_filter = ('branch', 'is_active', 'is_laboratory_analysis')
    search_fields = ('name',)
    list_per_page = 30
    ordering = ('tree_id', 'lft')  # MPTT order


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'price', 'is_active')
    list_filter = ('is_active', 'service__branch')
    search_fields = ('name', 'service__name')
    list_select_related = ('service',)
    list_per_page = 30
