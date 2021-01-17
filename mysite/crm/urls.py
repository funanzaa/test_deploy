from django.urls import path
from . import views
from .view_charts import get_data, ChartData, ChartDataService, ChartDataCase, MonthlyRecap
from .api import ControlVersionList, ControlVersionDetail, UserAuthentication ,ListSubProject


urlpatterns = [
    path('dashboard', views.dashboardPage, name='dashboard-page'),
    path('case/', views.viewCase, name='viewcase'),
    path('create_case/', views.createCase, name='create_case'),
    path('update_case/<str:pk>', views.updateCase, name='update_case'),
    path('detail/<str:pk>', views.detailCase, name='detail_case'),
    path('delete_case/<str:pk>', views.deleteCase, name='delete_case'),
    path('hospital/', views.hospital, name='hospital-page'),
    path('create_hospital/', views.hospitalAdd, name='create_hospital'),
    path('create_case_hospital/<str:pk>', views.create_case_hospital, name='create_case_hospital'),
    path('edit_hospital/<str:pk>', views.hospitalEdit, name='edit_hospital'),
    path('controlversions/', views.controlversions, name='controlversions-page'),
    # charts
    path('api/data/', get_data, name='get-data'),
    path('api/chart/data/', ChartData.as_view(), name='api-data'),
    path('api/chart_service/data/', ChartDataService.as_view(), name='api-data-service'),
    path('api/chart_case/data/', ChartDataCase.as_view(), name='api-data-case'),
    path('api/MonthlyRecap/data/', MonthlyRecap.as_view(), name='api-monthlyrecap'),


    # api subproject
    path('api/List_Subproject/<str:pk>/',views.List_Subproject, name='ListSubProject'),

    # Profile Server
    path('Profile_Server/',views.Profile_Server, name='Profile_Server'),
    path('ListProfileServer/',views.ListProfileServer, name='ListProfileServer'),
    path('SetupServer/<str:pk>/',views.SetupServer, name='SetupServer'),


    # controlVersions
    path('api/ControlVersionList/', ControlVersionList.as_view(), name='ControlVersion_List'),
    path('api/ControlVersionDetail/<str:pk>/', ControlVersionDetail.as_view(), name='ControlVersionDetail'),
    # Auth
    path('api/auth/', UserAuthentication.as_view(), name='User Authentication API')
]
