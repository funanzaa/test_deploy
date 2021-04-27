import datetime
import pytz
from .models import *
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView  # rest_framework
from rest_framework.response import Response  # rest_framework
from datetime import datetime, date
from dateutil.relativedelta import *
from .queryDashboard import *
import calendar

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

    # authentication_classes = []
    # permission_classes = []

    def get(self, request, format=None):

        data = {
            "labels": [],
            "default": [],
        }
        return Response(data)


class ChartDataService(APIView):

    # authentication_classes = []
    # permission_classes = []

    def get(self, request, format=None):
        labels = []
        default_items = []
        labelService = serviceCrm()

        for i in range(len(serviceCrm())): 
            labels.append(labelService[i][0])

        for j in range(len(labels)):
            default_items.append(countSevice(labels[j]))
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)


class ChartDataCase(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        # Reversing a list using reversed()
        def Reverse(lst):
            return [ele for ele in reversed(lst)]

        start_date = date.today()
        # print(start_date)
        number_of_days = 12
        date_list = []
        year_list = []
        month_list = []
        
        for month in range(number_of_days):
            a_date = (start_date - relativedelta(months =  month)).strftime("%b-%y")
            a_year = (start_date - relativedelta(months=  month)).strftime("%Y")
            a_month = (start_date - relativedelta(months=  month)).strftime("%m")
            date_list.append(a_date)
            year_list.append(a_year)
            month_list.append(a_month)  
        rev_month = Reverse(month_list)
        rev_year = Reverse(year_list)
        items = []

        # for i in range(len(rev_month)):
        #     items.append(caseOfYear(month=rev_month[i],year=rev_year[i]))

        # type zip
        for m , y in zip(rev_month, rev_year):
            items.append(caseOfYear(month=m ,year=y))

        labels = Reverse(date_list)
        data = {
            "labels": labels,
            "default": items,
        }
        return Response(data)


class MonthlyRecap(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        now = date.today()
        labels_list = []
        default_items = []

        for days in range(1,(calendar.monthrange(now.year, now.month)[1] + 1 )):
            labels_list.append(days)
            default_items.append(monthRecepReport(day = days,month = now.month ,year = now.year))

        data = {
            "labels": labels_list,
            "default": default_items,
        }
        return Response(data)
