from django.contrib import admin
from rango.models import Category, Page, UserProfile # Added by JNR 22.01.2018 - UserProfile on 29.01.2018

# Add in this class to customise the admin interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Added to modify the page content
class PageAdmin (admin.ModelAdmin): # Added by JNR 23.01.2018
    list_display = ('title','category','url')

# Register your models here.

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile) # Added by JNR 29.01.2018
