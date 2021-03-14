from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse_lazy
import datetime
import pytz
import requests
import json
from .query import *

def insertAPIBkk(request):
    tz = pytz.timezone('Asia/Bangkok')
    url = 'https://bkkapp.nhso.go.th/bkkapp/api/v1/public/HelpdeskReportService/get_list_callback_new'
    respones = requests.get(url)
    d = respones.json()
    for i in range(len(d['record'])):
        newCaseApi = ApiAppNhsoBkk()
        newCaseApi.callback_id = d['record'][i]['CALLBACK_ID']	
        newCaseApi.callback_code = d['record'][i]['CALLBACK_CODE']
        newCaseApi.callback_title = d['record'][i]['CALLBACK_TITLE']
        newCaseApi.callback_group_id = d['record'][i]['CALLBACK_GROUP_ID']
        newCaseApi.callback_subgroup_id = d['record'][i]['CALLBACK_SUBGROUP_ID']
        newCaseApi.callback_tag = d['record'][i]['CALLBACK_TAG']
        newCaseApi.staff_id = d['record'][i]['STAFFID']
        newCaseApi.profile = d['record'][i]['PROFILE']
        newCaseApi.callback_name = d['record'][i]['CALLBACK_NAME']
        newCaseApi.mobile_phone = d['record'][i]['MOBILE_PHONE']
        newCaseApi.detail = d['record'][i]['DETAIL']
        newCaseApi.insert_at = datetime.datetime.now(tz=tz)
        newCaseApi.save()
        postStatus2(d['record'][i]['CALLBACK_CODE'])
    return HttpResponse("OK")

def ListAPIBkk(request):
    context = {
        "ListinsertApi":ListinsertApi()
        ,"countNotificationsAPI":countNotificationsAPI()
        ,"TimeApiInsert":TimeApiInsert()
        }
    return render(request,'apiCases/ListAPI.html',context)


