from django.contrib import admin
from .models import *

admin.site.register(Project)
admin.site.register(Project_subgroup)
admin.site.register(Hospitals)
admin.site.register(Service)
admin.site.register(Case)