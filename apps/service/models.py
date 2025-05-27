import string

from django.core.exceptions import ValidationError
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


# Create your models here.


class Service(MPTTModel):
    """
    Xizmatlar va kategoriyalar daraxtsimon tuzilma sifatida saqlanadi.
    Kategoriya: parent = None
    Xizmat: parent != None
    """
    branch = models.ForeignKey(
        'main.ClinicBranch', on_delete=models.CASCADE, related_name='branch_services', blank=True, null=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Nomi",
        help_text="Xizmat yoki kategoriya nomi (masalan: Laboratoriya, Qon tahlillari)."
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Ota kategoriya",
        help_text="Agar bu obyekt boshqa kategoriya ostida bo‘lsa, ota kategoriyani tanlang."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faollik holati",
        help_text="Faol xizmat yoki kategoriya ekanligini belgilang."
    )
    is_laboratory_analysis = models.BooleanField(
        default=True,
        verbose_name="Labaratoriya analizi.",
        help_text="Labaratoriya analizi."
    )
    queue_letter = models.CharField(
        max_length=1,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Navbat harfi",
        help_text="Bu xizmat uchun navbat harfi (masalan: A, B, C)"
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Xizmat yoki Kategoriya"
        verbose_name_plural = "Xizmatlar va Kategoriyalar"
        db_table = "logics"
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'queue_letter'],
                name='unique_queue_letter_per_branch'
            )
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent is None:
            if not self.queue_letter and self.branch:
                used_letters = Service.objects.filter(
                    branch=self.branch,
                    parent__isnull=True
                ).exclude(pk=self.pk).values_list('queue_letter', flat=True)

                used_letters = set(filter(None, used_letters))

                for letter in string.ascii_uppercase:
                    if letter not in used_letters:
                        self.queue_letter = letter
                        break
                else:
                    raise ValidationError("Ushbu filialda barcha A-Z harflari band.")
        else:
            self.queue_letter = None

        super().save(*args, **kwargs)


class ServiceItem(models.Model):
    """
    Aniq xizmat elementi: laboratoriya, davolash yoki shifokor qabuli.
    """
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Xizmat",
        help_text="Ushbu element qaysi xizmatga tegishli ekanligini ko‘rsating."
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Element nomi",
        help_text="Xizmat elementi nomi (masalan: Glyukoza tahlili, Konsultatsiya)."
    )
    price = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name="Narxi (so‘mda)",
        help_text="Agar variantlar ishlatilmasa, bu yerda xizmat narxini belgilang."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faollik holati",
        help_text="Xizmat elementi faol ekanligini belgilang."
    )

    class Meta:
        verbose_name = "Xizmat elementi"
        verbose_name_plural = "Xizmat elementlari"
        db_table = "service_items"

    def __str__(self):
        return f"{self.service.name} - {self.name}"
