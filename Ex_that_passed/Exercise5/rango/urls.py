from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # Created by JNR 18.01.2018
    url(r'^about/', views.about, name='about'), # Created by JNR 18.01.2018
]
