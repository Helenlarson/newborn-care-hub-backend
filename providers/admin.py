# Register your models here.
from django.contrib import admin
from .models import ServiceType, ProfessionalProfile

admin.site.register(ServiceType)
admin.site.register(ProfessionalProfile)

