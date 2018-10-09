from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.home, name = 'home'),
    url('response', views.get_response, name = 'get_response'),
]
