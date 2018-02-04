from django.contrib import admin
from rango.models import Category, Page # Added by JNR 22.01.2018

# Added to modify the page content

class PageAdmin (admin.ModelAdmin): # Added by JNR 23.01.2018
    list_display = ('title','category','url')

# Register your models here.

admin.site.register(Category)
admin.site.register(Page, PageAdmin)

