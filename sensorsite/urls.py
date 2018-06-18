from django.conf.urls import include, url

from django.contrib import admin, admindocs
from django.contrib.admindocs import urls as admindocs_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'sensors.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^lab/', include('labenviron.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include(admindocs_urls)),
]
