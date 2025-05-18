from django.db import models


class ClinicBranch(models.Model):
    name = models.CharField(max_length=255, verbose_name="Filial nomi")
    address = models.TextField(verbose_name="Manzil")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Telefon raqami")

    class Meta:
        verbose_name = "Klinika filiali"
        verbose_name_plural = "Klinika filiallari"

    def __str__(self):
        return self.name
