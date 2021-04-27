from django.urls import path
from .views import *

app_name = 'profileErefer'

urlpatterns = [
     path('requestSetupErefer/',requestSetupErefer, name= 'requestSetupErefer'),
     path('SetupErefer/',SetupErefer, name= 'SetupErefer'),
     path('install_Erefer/<int:pk>/',install_Erefer, name= 'install_Erefer'), #
     path('updateEreferProfile/<int:pk>/',updateEreferProfile, name= 'updateEreferProfile'), #
     path('setupStatus/<int:pk>/',setupStatus, name= 'setupStatus'),
     path('setupStatus1/',setupStatus_1, name= 'setupStatus1'),
     path('check_case_lock/<int:pk>/',check_case_lock, name= 'check_case_lock'), # lock case
     path('viewAllErefer/',viewAllErefer, name= 'viewAllErefer'),
     path('overAllHc/',OverAllHc, name= 'overAllHc'),
     # export csv
     path('export_ereferral_csv/',export_ereferral_csv, name= 'export_ereferral_csv'),
]