from django.conf.urls import url
from rango import views

app_name = 'rango' # Added by JNR 25.01.2018
urlpatterns = [
    url(r'^$', views.index, name='index'), # Created by JNR 18.01.2018
    url(r'^about/$', views.about, name='about'), # Created by JNR 18.01.2018
    url(r'^add_category/$', views.add_category, name='add_category'), # Added 23.01.2018
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'), # Added by JNR 23.01.2018
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'), # Added by JNR 23.01.2018
    url(r'^register/$', views.register, name='register'), # Added by JNR 29.01.2018
    url(r'^login/$', views.user_login, name='login'), # Added by JNR 29.01.2018
    url(r'^restricted/$', views.restricted, name='restricted'), # Added by JNR 29.01.2018
    url(r'^logout/$', views.user_logout, name='logout'), # Added by JNR 29.01.2018
]
