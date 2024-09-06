from django.contrib import admin
from .models import UserProfile, Employee, Restaurant

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Employee)
admin.site.register(Restaurant)