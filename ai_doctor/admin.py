from django.contrib import admin
from . import models


# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Doctor, DoctorAdmin)


class AppointmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Appointment, AppointmentAdmin)
