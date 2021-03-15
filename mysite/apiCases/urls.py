from django.urls import path
from .views import *

app_name = 'apiCases'

urlpatterns = [
     path('insert/',insertAPIBkk, name= 'insert'),
     path('ListAPIBkk/',ListAPIBkk, name= 'ListApiBkk'),
     path('createCaseApi/',createCaseApi, name= 'createCaseApi'),
]