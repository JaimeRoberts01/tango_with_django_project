from django import template # Created by JNR 28.01.2018
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/cats.html') 

def get_category_list(cat=None): # Modified by JNR 28.01.2018
	return {'cats': Category.objects.all(), 'act_cat': cat} # Modified by JNR 28.01.2018
