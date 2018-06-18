from django.conf.urls import url

from . import views

app_name = 'labenviron'

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^plot$', views.plot, name='plot'),
  url(r'^data$', views.data, name='data'),
]
