"""SiteCrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf.urls.static import static #  2 set image
from django.conf import settings #  3 set image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage, name="home"),
    path('about/', views.AboutPage, name="about"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('crm/', include('crm.urls')),
    path('model5/dashboard/', views.model5_dashboard, name="model5_dashboard"),
    path('model5/hosp_model5/', views.hosp_model5, name="hosp_model5"),
    path('model5/lookup_error/', views.lookup_error, name="lookup_error"),
    path('model5/recepreport/', views.recepreport, name="recepreport"),
    path('model5/installApp', views.installApp, name="installApp"),
    path('model5/training', views.training, name="training"),
    path('model5/amountHospReqClaimcode', views.amountHospReqClaimcode, name="amountHospReqClaimcode"),
    path('model5/amountHospReqClaim', views.amountHospReqClaim, name="amountHospReqClaim"),
    path('model5/amountDataHospReqClaimCode', views.amountDataHospReqClaimCode, name="amountDataHospReqClaimCode"),
    path('model5/amountDataHospReqClaim', views.amountDataHospReqClaim, name="amountDataHospReqClaim"),
    path('model5/HospApprove', views.HospApprove, name="HospApprove"),
    path('model5/ErrorDetail', views.ErrorDetail, name="model5Error"),
    path('model5/ErrorDetail/<str:hcode>', views.ErrorDetailHcode, name='ErrorDetailHcode'),
    path('model5/ListHospNotClaim', views.ListHospNotClaim, name="ListHospNotClaim"),
    path('model5/dataKnowReqClaimCode', views.dataKnowReqClaimCode, name="dataKnowReqClaimCode"),
    path('model5/dataTimePeriodOver', views.dataTimePeriodOver, name="dataTimePeriodOver"),
    path('model5/dataTimePeriodUnder', views.dataTimePeriodUnder, name="dataTimePeriodUnder"),
    # chart
    path('api/model5HospSendClaimCode/data/', views.ChartHospSendClaimCode.as_view(), name='api-model5HospSendClaimCode'),
    path('api/model5AmountHospSendClaim/data/', views.ChartAmountHospSendClaim.as_view(), name='api-model5HospSendAmountClaim'),


]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) # 1 set image
