from django.urls import path
from .views import *

app_name = 'profileErefer'

urlpatterns = [
     path('requestSetupErefer/',requestSetupErefer, name= 'requestSetupErefer'),
     path('SetupErefer/',SetupErefer, name= 'SetupErefer'),
     path('install_Erefer/<int:pk>/',install_Erefer, name= 'install_Erefer'),
]