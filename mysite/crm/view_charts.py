import datetime
import pytz
from .models import *
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView  # rest_framework
from rest_framework.response import Response  # rest_framework


User = get_user_model()


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html', {"customers": 10})


def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data)  # http response


class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        tz = pytz.timezone('Asia/Bangkok')
        now = (datetime.datetime.now(tz=tz))
        if len(str(now)[5:7]) == 2:
            count_case_hos = count_case_hos = Case.objects.filter(date_entered__month=str(
                now)[5:7], project_id=1, date_entered__year=str(now)[:4]).count()
            count_project_opbkk = Case.objects.filter(date_entered__month=str(
                now)[5:7], project_id=2, date_entered__year=str(now)[:4]).count()
            count_project_erefer = Case.objects.filter(date_entered__month=str(
                now)[5:7], project_id=3, date_entered__year=str(now)[:4]).count()
            count_project_ehhc = Case.objects.filter(date_entered__month=str(
                now)[5:7], project_id=4, date_entered__year=str(now)[:4]).count()
            count_project_hshv = Case.objects.filter(date_entered__month=str(
                now)[5:7], project_id=5, date_entered__year=str(now)[:4]).count()
            count_project_smartcard = Case.objects.filter(date_entered__month=str(
                now)[5:7], project_id=6, date_entered__year=str(now)[:4]).count()
            count_server = Case.objects.filter(date_entered__month=str(
                now)[5:7], project_id=7, date_entered__year=str(now)[:4]).count()
            count_other = Case.objects.filter(date_entered__month=str(
                now)[5:7], project_id=8, date_entered__year=str(now)[:4]).count()
        else:
            count_case_hos = count_case_hos = Case.objects.filter(date_entered__month=str(
                now)[6:7], project_id=1, date_entered__year=str(now)[:4]).count()
            count_project_opbkk = Case.objects.filter(date_entered__month=str(
                now)[6:7], project_id=2, date_entered__year=str(now)[:4]).count()
            count_project_erefer = Case.objects.filter(date_entered__month=str(
                now)[6:7], project_id=3, date_entered__year=str(now)[:4]).count()
            count_project_ehhc = Case.objects.filter(date_entered__month=str(
                now)[6:7], project_id=4, date_entered__year=str(now)[:4]).count()
            count_project_hshv = Case.objects.filter(date_entered__month=str(
                now)[6:7], project_id=5, date_entered__year=str(now)[:4]).count()
            count_project_smartcard = Case.objects.filter(date_entered__month=str(
                now)[6:7], project_id=6, date_entered__year=str(now)[:4]).count()
            count_server = Case.objects.filter(date_entered__month=str(
                now)[6:7], project_id=7, date_entered__year=str(now)[:4]).count()
            count_other = Case.objects.filter(date_entered__month=str(
                now)[6:7], project_id=8, date_entered__year=str(now)[:4]).count()

        labels = ['HospitalOS', 'OPBKKClaim', 'Ereferral',
                  'EHHC', 'HsHv', 'SmartCard', 'Server', 'Other']
        default_items = [count_case_hos, count_project_opbkk, count_project_erefer,
                         count_project_ehhc, count_project_hshv, count_project_smartcard, count_server, count_other]
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)


class ChartDataService(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        tz = pytz.timezone('Asia/Bangkok')
        now = (datetime.datetime.now(tz=tz))
        if len(str(now)[5:7]) == 2:
            count_call = Case.objects.filter(date_entered__month=str(
                now)[5:7], service_id=1, date_entered__year=str(now)[:4]).count()
            count_line = Case.objects.filter(date_entered__month=str(
                now)[5:7], service_id=2, date_entered__year=str(now)[:4]).count()
            count_facebook = Case.objects.filter(date_entered__month=str(
                now)[5:7], service_id=3, date_entered__year=str(now)[:4]).count()
            count_email = Case.objects.filter(date_entered__month=str(
                now)[5:7], service_id=4, date_entered__year=str(now)[:4]).count()
            count_Line_official = Case.objects.filter(date_entered__month=str(
                now)[5:7], service_id=5, date_entered__year=str(now)[:4]).count()
        else:
            count_call = Case.objects.filter(date_entered__month=str(
                now)[6:7], service_id=1, date_entered__year=str(now)[:4]).count()
            count_line = Case.objects.filter(date_entered__month=str(
                now)[6:7], service_id=2, date_entered__year=str(now)[:4]).count()
            count_facebook = Case.objects.filter(date_entered__month=str(
                now)[6:7], service_id=3, date_entered__year=str(now)[:4]).count()
            count_email = Case.objects.filter(date_entered__month=str(
                now)[6:7], service_id=4, date_entered__year=str(now)[:4]).count()
            count_Line_official = Case.objects.filter(date_entered__month=str(
                now)[6:7], service_id=5, date_entered__year=str(now)[:4]).count()

        labels = ['Call', 'line', 'facebook', 'email', 'Line_official']
        default_items = [count_call, count_line, count_facebook, count_email, count_Line_official]
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)


class ChartDataCase(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        tz = pytz.timezone('Asia/Bangkok')
        now = (datetime.datetime.now(tz=tz))
        count_m9 = Case.objects.filter(date_entered__month='9',
                                       date_entered__year=str(now)[:4]).count()
        count_m10 = Case.objects.filter(date_entered__month='10',
                                        date_entered__year=str(now)[:4]).count()
        count_m11 = Case.objects.filter(date_entered__month='11',
                                        date_entered__year=str(now)[:4]).count()
        count_m12 = Case.objects.filter(date_entered__month='12',
                                        date_entered__year=str(now)[:4]).count()
        count_m01 = Case.objects.filter(date_entered__month='1',
                                        date_entered__year=str(now)[:4]).count()
        count_m02 = Case.objects.filter(date_entered__month='2',
                                        date_entered__year=str(now)[:4]).count()
        count_m03 = Case.objects.filter(date_entered__month='3',
                                        date_entered__year=str(now)[:4]).count()
        count_m04 = Case.objects.filter(date_entered__month='4',
                                        date_entered__year=str(now)[:4]).count()
        count_m05 = Case.objects.filter(date_entered__month='5',
                                        date_entered__year=str(now)[:4]).count()
        count_m06 = Case.objects.filter(date_entered__month='6',
                                        date_entered__year=str(now)[:4]).count()
        count_m07 = Case.objects.filter(date_entered__month='7',
                                        date_entered__year=str(now)[:4]).count()
        count_m08 = Case.objects.filter(date_entered__month='8',
                                        date_entered__year=str(now)[:4]).count()

        labels = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb',
                  'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', ]
        default_items = [count_m9, count_m10, count_m11, count_m12, count_m01,
                         count_m02, count_m03, count_m04, count_m05, count_m06, count_m07, count_m08]
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)


class MonthlyRecap(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        tz = pytz.timezone('Asia/Bangkok')
        now = (datetime.datetime.now(tz=tz))
        labels_list = []
        default_items = []
        i = 1
        Cases = Case.objects.filter(date_entered__year=now.year, date_entered__month=now.month).count()
        if Cases == 0:
            data = {
            "labels": [Cases],
            "default": [Cases],
        }
            return Response(Cases)
        else:
            while i <= now.day:
                labels_list.append(str(i))
                default_items.append(Case.objects.filter(
                    date_entered__year=now.year, date_entered__month=now.month, date_entered__day=i).count())
                i += 1
            data = {
                "labels": labels_list,
                "default": default_items,
            }
            return Response(data)
