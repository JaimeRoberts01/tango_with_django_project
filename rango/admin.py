from django.contrib import admin
from rango.models import Category, Page # Added by JNR 22.01.2018

# Register your models here.

admin.site.register(Category)
admin.site.register(Page)