from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    pass


class Conv(models.Model):
    user_message = models.CharField(max_length=1000)
    response = models.CharField(max_length=1000)


class Doctor(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    speciality = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    number = models.CharField(max_length=64)
    profile_photo = models.ImageField(default="fallback.png", blank=True)
    description = models.TextField(
        default="""Dr. John is a skilled and compassionate dentist known for his patient-centered approach and expertise in comprehensive oral care.
                With years of experience, Dr. John has built a reputation for delivering high-quality dental services,
                including routine cleanings, advanced restorative work, and cosmetic dentistry."""
    )


class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
