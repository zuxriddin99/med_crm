from django.db import models

from apps.base_app.models import BaseModel
import locale
from service_logics.utils import format_price_as_str, get_formated_phone_number, format_datetime_uz


# Create your models here.
class Client(BaseModel):
    first_name = models.CharField(
        max_length=150, default='', blank=True, verbose_name="Ismi"
    )
    last_name = models.CharField(
        max_length=150, default='', blank=True, verbose_name="Familiyasi"
    )
    phone_number = models.CharField(
        max_length=15, default='', blank=True, verbose_name="Telefon raqami"
    )
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name="Tug‘ilgan sanasi"
    )
    address = models.CharField(
        max_length=350, default='', blank=True, verbose_name="Manzili"
    )
    workplace = models.CharField(
        max_length=250, default='', blank=True, verbose_name="Ish joyi"
    )
    description = models.TextField(
        default='', blank=True, verbose_name="Qo‘shimcha izoh"
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.date_of_birth}'

    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"
        db_table = 'clients'

    @property
    def translated_date_of_birth(self):
        if self.date_of_birth:
            locale.setlocale(locale.LC_TIME, 'uz_UZ.UTF-8')
            return self.date_of_birth.strftime('%Y-yil %d-%b')
        return ""

    @property
    def translated_created_at(self):
        return format_datetime_uz(self.created_at)

    @property
    def formated_phone_number(self):
        return get_formated_phone_number(self.phone_number)

    @property
    def phone_number_without_suffix(self):
        if self.phone_number.startswith("+998") and len(self.phone_number) == 13:
            return self.phone_number.replace("+998", "")
