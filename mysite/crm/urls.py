from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.dashboardPage, name='dashboard-page'),
    path('create_case/', views.createCase, name='create_case'),
    path('update_case/<str:pk>', views.updateCase, name='update_case'),
    path('delete_case/<str:pk>', views.deleteCase, name='delete_case'),
    path('hospital/', views.hospital, name='hospital-page'),
    path('create_hospital/', views.hospitalAdd, name='create_hospital'),
    path('create_case_hospital/<str:pk>', views.create_case_hospital, name='create_case_hospital'),
    path('edit_hospital/<str:pk>', views.hospitalEdit, name='edit_hospital'),
]
