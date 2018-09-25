from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home', views.home, name = 'home'),
    url(r'^response', views.get_response, name = 'get_response'),
]