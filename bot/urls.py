from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('response', views.get_response, name='get_response'),
#     path('plot', views.plot, name = 'plot'),
#     path('rainfall_patterns', views.rainfall_patterns, name = 'rainfall_patterns'),
]
