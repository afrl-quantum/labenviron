from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^all$', views.all),
  url(r'^day/(?P<day>\d{8})$', views.day),
]
