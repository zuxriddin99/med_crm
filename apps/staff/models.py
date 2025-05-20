from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class StaffRole(models.TextChoices):
    DOCTOR = 'doctor', 'Shifokor'
    RECEPTIONIST = 'receptionist', 'Registrator'
    LAB_TECH = 'lab_tech', 'Labaratoriya hodimi'
    ADMIN = 'admin', 'Administrator'


class StaffUser(AbstractUser):
    role = models.CharField(
        max_length=30, choices=StaffRole.choices)
    branch = models.ForeignKey(
        'main.ClinicBranch', on_delete=models.CASCADE, related_name='staff', blank=True, null=True
    )
    REQUIRED_FIELDS = []
    providing_services = models.ManyToManyField("service.Service", related_name='staff', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Xodim"
        verbose_name_plural = "Xodimlar"
        db_table = 'staff_users'

    def is_admin(self):
        return self.role == StaffRole.ADMIN
