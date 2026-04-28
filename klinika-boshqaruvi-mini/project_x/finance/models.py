from django.db import models
from .base_model import BaseModel


class Doctor(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Doctors"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Consultation(BaseModel):

    CHOICES = {
        "korik": "Ko`rik",
        "qaytakorik": "Qayta ko`rik",
    }

    type = models.CharField(max_length=50, choices=CHOICES)
    date = models.DateTimeField(blank=True)
    doctor_percent = models.DecimalField(max_digits=5, decimal_places=2)
    minus_beshming = models.PositiveIntegerField(default=5000, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.PositiveIntegerField()
    doctor = models.ForeignKey(Doctor, null=True, related_name='consultations', on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.id} | {self.type}"


class Surgery(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    surgery_expense = models.DecimalField(max_digits=10, decimal_places=2)
    doctor_percent = models.DecimalField(max_digits=5, decimal_places=2)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL, related_name='surgeries')
    date = models.DateTimeField(blank=True)
    receipt_number = models.PositiveIntegerField()


    class Meta:
        verbose_name_plural = "Surgeries"

    def __str__(self):
        return 'Operatsiya'


class Room(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    doctor_percent = models.DecimalField(max_digits=5, decimal_places=2)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL, related_name='rooms')
    date = models.DateTimeField(blank=True)
    receipt_number = models.PositiveIntegerField(blank=True, null=True)


    class Meta:
        verbose_name_plural = "Rooms"

    def __str__(self):
        return 'Palata'

