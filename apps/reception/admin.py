from django.contrib import admin
from django.utils.html import format_html

from apps.reception.models import ReferralPerson, Visit, VisitItem, VisitItemDiagnosis, DiagnosisTemplate


@admin.register(ReferralPerson)
class ReferralPersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'formated_phone_number', 'additional_information')
    search_fields = ('full_name', 'phone_number')
    list_per_page = 25


class VisitItemInline(admin.TabularInline):
    model = VisitItem
    extra = 0
    readonly_fields = ('service_item', 'doctor', 'price')
    can_delete = False
    show_change_link = True


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('client', 'branch', 'created_at', 'is_completed', 'discount_str', 'access_code')
    list_filter = ('branch', 'is_completed', 'created_at')
    search_fields = ('client__full_name', 'access_code')
    readonly_fields = ('access_code', 'created_at', 'updated_at')
    inlines = [VisitItemInline]
    date_hierarchy = 'created_at'
    list_per_page = 30


class VisitItemDiagnosisInline(admin.StackedInline):
    model = VisitItemDiagnosis
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    can_delete = False


@admin.register(VisitItem)
class VisitItemAdmin(admin.ModelAdmin):
    list_display = ('visit', 'service_item', 'doctor', 'price')
    search_fields = ('visit__client__full_name', 'service_item__name')
    list_filter = ('doctor', 'service_item')
    inlines = [VisitItemDiagnosisInline]
    list_per_page = 30


@admin.register(VisitItemDiagnosis)
class VisitItemDiagnosisAdmin(admin.ModelAdmin):
    list_display = ('visit_item_link', 'author', 'short_diagnosis', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('diagnosis', 'recommendations', 'visit_item__visit__client__full_name')
    list_filter = ('author', 'created_at')
    list_per_page = 30

    def short_diagnosis(self, obj):
        return format_html(obj.diagnosis[:60] + "..." if len(obj.diagnosis) > 60 else obj.diagnosis)
    short_diagnosis.short_description = "Tashxis (qisqa)"

    def visit_item_link(self, obj):
        return format_html(
            '<a href="/admin/{}/{}/{}/change/">{}</a>',
            obj.visit_item._meta.app_label,
            obj.visit_item._meta.model_name,
            obj.visit_item.pk,
            str(obj.visit_item)
        )
    visit_item_link.short_description = "Qabul elementi"

@admin.register(DiagnosisTemplate)
class DiagnosisTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_item', 'created_by', 'is_active', 'created_at')
    list_filter = ('is_active', 'service_item')
    search_fields = ('title', 'diagnosis', 'recommendations')
    list_select_related = ('service_item', 'created_by')
    list_per_page = 30
