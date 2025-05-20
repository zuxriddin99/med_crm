import random
import string
import locale

from django.db import models

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
    registered_by = models.ForeignKey("staff.StaffUser", on_delete=models.SET_NULL, null=True, related_name='visits_registered')
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
        while True:
            code = random.choices(string.ascii_uppercase, k=2) + random.choices(string.digits, k=4)
            random.shuffle(code)
            code = ''.join(code)
            if not Visit.objects.filter(access_code=code).exists():
                return code

    class Meta:
        verbose_name = "Qabul"
        verbose_name_plural = "Qabullar"
        db_table = "receptions"

    def __str__(self):
        return f"{self.client} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @property
    def translated_created_at(self):
        return format_datetime_uz(self.created_at)

    @property
    def discount_str(self):
        return format_price_as_str(self.discount)

