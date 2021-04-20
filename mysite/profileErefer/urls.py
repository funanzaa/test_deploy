from django.urls import path
from .views import *

app_name = 'profileErefer'

urlpatterns = [
     path('requestSetupErefer/',requestSetupErefer, name= 'requestSetupErefer'),
     path('SetupErefer/',SetupErefer, name= 'SetupErefer'),
     path('install_Erefer/<int:pk>/',install_Erefer, name= 'install_Erefer'),
     path('updateEreferProfile/<int:pk>/',updateEreferProfile, name= 'updateEreferProfile'),
     path('setupStatus/<int:pk>/',setupStatus, name= 'setupStatus'),
     path('setupStatus/',check_case_lock, name= 'check_case_lock'),
     path('viewAllErefer/',viewAllErefer, name= 'viewAllErefer'),
     path('overAllHc/',OverAllHc, name= 'overAllHc'),
]