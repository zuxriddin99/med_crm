from django.db import models

from apps.base_app.models import BaseModel
import locale


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
        if self.created_at:
            locale.setlocale(locale.LC_TIME, 'uz_UZ.UTF-8')
            return self.created_at.strftime('%Y-yil %-d-%b %H:%M')
        return ""

    @property
    def formated_phone_number(self):
        if self.phone_number.startswith("+998") and len(self.phone_number) == 13:
            return f"{self.phone_number[:4]} ({self.phone_number[4:6]}) {self.phone_number[6:9]} {self.phone_number[9:11]} {self.phone_number[11:]}"
        else:
            return self.phone_number if self.phone_number else "-"

    @property
    def phone_number_without_suffix(self):
        if self.phone_number.startswith("+998") and len(self.phone_number) == 13:
            return self.phone_number.replace("+998", "")
