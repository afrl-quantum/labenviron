from django.contrib import admin
from .models import *

# Register your models here.
class HostInfoAdmin(admin.ModelAdmin):
  #list_per_page = 25
  list_display = ('host', 'location', 'comments')
  list_display_links = ('host', )
  list_editable= ('location', )

class LabDataAdmin(admin.ModelAdmin):
  #list_per_page = 25
  list_display = ('host', 'time', 'temperature', 'pressure', 'humidity')
  list_display_links = ('time', )
  list_editable= ('host', )

admin.site.register(HostInfo, HostInfoAdmin)
admin.site.register(LabData, LabDataAdmin)
