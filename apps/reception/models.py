import random
import string
import locale

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from apps.base_app.models import BaseModel
from logics.utils import format_price_as_str, get_formated_phone_number, format_datetime_uz


# Create your models here.

class ReferralPerson(BaseModel):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, default='')
    additional_information = models.TextField(blank=True, default='')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Referral Person'
        verbose_name_plural = 'Referral Persons'
        db_table = 'referral_persons'

    @property
    def formated_phone_number(self):
        return get_formated_phone_number(self.phone_number)


class Visit(BaseModel):
    """
        Mijoz tashrifini qayd etuvchi model (Qabul).
    """
    client = models.ForeignKey(
        "client.Client",
        on_delete=models.CASCADE,
        related_name='receptions',
        verbose_name="Mijoz",
        help_text="Tashrif buyurgan mijozni tanlang."
    )
    registered_by = models.ForeignKey("staff.StaffUser", on_delete=models.SET_NULL, null=True,
                                      related_name='visits_registered')
    discount = models.IntegerField(
        default=0,
        verbose_name="Chegirma (so‘mda)",
        help_text="Agar mavjud bo‘lsa, mijozga berilgan chegirma summasini kiriting."
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Izoh",
        help_text="Qabul haqida qo‘shimcha izoh (ixtiyoriy)."
    )

    is_completed = models.BooleanField(default=False)
    access_code = models.CharField(max_length=10, unique=True, blank=True, null=True, )
    branch = models.ForeignKey("main.ClinicBranch", on_delete=models.CASCADE)

    @staticmethod
    def generate_unique_access_code():
        while True:  # todo bad idea need optimize. Maybe infinity loop
            code = random.choices(string.ascii_uppercase, k=2) + random.choices(string.digits, k=4)
            random.shuffle(code)
            code = ''.join(code)
            if not Visit.objects.filter(access_code=code).exists():
                return code

    class Meta:
        verbose_name = "Qabul"
        verbose_name_plural = "Qabullar"
        db_table = "visits"

    def __str__(self):
        return f"{self.client} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @property
    def created_at_str(self):
        return format_datetime_uz(self.created_at)

    @property
    def discount_str(self):
        return format_price_as_str(self.discount)

    @property
    def client_full_name(self):
        return f"{self.client.last_name} {self.client.first_name}"


class VisitItem(BaseModel):
    visit = models.ForeignKey(
        Visit, on_delete=models.CASCADE, related_name='items',
    )
    service_item = models.ForeignKey(
        'service.ServiceItem',
        on_delete=models.CASCADE,
        related_name='visit_items',
        verbose_name="Xizmat elementi",
        help_text="Mijoz tanlagan xizmat elementi."
    )
    price = models.IntegerField(
        default=0,
        verbose_name="Narxi (so‘mda)",
        help_text="Ushbu xizmat (yoki varianti) bo‘yicha to‘langan summa."
    )
    doctor = models.ForeignKey(
        "staff.StaffUser", on_delete=models.SET_NULL, null=True, related_name='visit_items'
    )

    class Meta:
        verbose_name = 'Qabul elementi'
        verbose_name_plural = 'Qabul elementlari'
        db_table = "visit_items"


class VisitItemDiagnosis(BaseModel):
    visit_item = models.ForeignKey(
        'VisitItem',
        on_delete=models.CASCADE,
        related_name='diagnoses',
        verbose_name="Qabul elementi"
    )
    author = models.ForeignKey(
        "staff.StaffUser",
        on_delete=models.PROTECT,
        verbose_name="Shifokor"
    )
    diagnosis = CKEditor5Field(
        verbose_name="Tashxis",
        help_text="Aniqlangan kasallik yoki holat"
    )
    recommendations = CKEditor5Field(
        verbose_name="Tavsiyalar",
        help_text="Davolash, tekshiruv yoki boshqa tavsiyalar"
    )

    class Meta:
        verbose_name = "Diagnostika"
        verbose_name_plural = "Diagnostikalar"
        db_table = "visit_item_diagnoses"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.visit_item} | {self.author} | {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class DiagnosisTemplate(BaseModel):
    service_item = models.ForeignKey(
        'service.ServiceItem',
        on_delete=models.CASCADE,
        related_name='diagnosis_templates',
        verbose_name="Xizmat elementi",
        help_text="Bu tashxis shabloni qaysi xizmatga tegishli."
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Sarlavha",
        help_text="Shablon sarlavhasi (masalan: Diabet tashxisi)"
    )
    diagnosis = CKEditor5Field(
        verbose_name="Tashxis matni",
        help_text="Tashxis matni (CKEditor5 orqali)"
    )
    recommendations = CKEditor5Field(
        verbose_name="Tavsiyalar matni",
        help_text="Tavsiya yoki davolash yo‘riqlari"
    )
    created_by = models.ForeignKey(
        "staff.StaffUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_templates",
        verbose_name="Yaratgan shifokor"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tashxis shabloni"
        verbose_name_plural = "Tashxis shablonlari"
        db_table = "diagnosis_templates"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.service_item.name} | {self.title}"
