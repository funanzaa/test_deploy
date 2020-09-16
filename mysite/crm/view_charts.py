import datetime
import pytz
from .models import *
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView  # rest_framework
from rest_framework.response import Response # rest_framework



User = get_user_model()

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html', {"customers":10})

def get_data(request,*args, **kwargs):
    data = {
        "sales":100,
        "customers":10,
    }
    return JsonResponse(data) # http response


class ChartData(APIView):

    authentication_classes = []
    permission_classes = []


    def get(self, request, format=None):
        tz = pytz.timezone('Asia/Bangkok')
        now = (datetime.datetime.now(tz=tz))
        count_case_hos = count_case_hos = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=1,date_entered__year=str(now)[:4]).count()
        count_project_opbkk = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=2,date_entered__year=str(now)[:4]).count()
        count_project_erefer = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=3,date_entered__year=str(now)[:4]).count()
        count_project_ehhc = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=4,date_entered__year=str(now)[:4]).count()
        count_project_hshv = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=5,date_entered__year=str(now)[:4]).count()
        count_project_smartcard = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=6,date_entered__year=str(now)[:4]).count()
        count_server = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=7,date_entered__year=str(now)[:4]).count()
        count_other = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=8,date_entered__year=str(now)[:4]).count()

        labels = ['HospitalOS', 'OPBKKClaim', 'Ereferral', 'EHHC', 'HsHv', 'SmartCard','Server','Other']
        default_items = [count_case_hos, count_project_opbkk, count_project_erefer
        , count_project_ehhc,count_project_hshv,count_project_smartcard,count_server,count_other]
        data = {
            "labels":labels,
            "default":default_items,
        }
        return Response(data)

class ChartDataService(APIView):

    authentication_classes = []
    permission_classes = []


    def get(self, request, format=None):
        tz = pytz.timezone('Asia/Bangkok')
        now = (datetime.datetime.now(tz=tz))
        count_call = count_case_hos = Case.objects.filter(date_entered__month=str(now)[6:7],service_id=1,date_entered__year=str(now)[:4]).count()
        count_line= Case.objects.filter(date_entered__month=str(now)[6:7],service_id=2,date_entered__year=str(now)[:4]).count()
        count_facebook = Case.objects.filter(date_entered__month=str(now)[6:7],service_id=3,date_entered__year=str(now)[:4]).count()
        count_email = Case.objects.filter(date_entered__month=str(now)[6:7],service_id=4,date_entered__year=str(now)[:4]).count()
        count_Line_official = Case.objects.filter(date_entered__month=str(now)[6:7],service_id=5,date_entered__year=str(now)[:4]).count()

        labels = ['Call', 'line', 'facebook', 'email', 'Line_official']
        default_items = [count_call, count_line, count_facebook
        , count_email,count_Line_official]
        data = {
            "labels":labels,
            "default":default_items,
        }
        print("view:ddd",data)
        return Response(data)
