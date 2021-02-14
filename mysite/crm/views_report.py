import datetime
import pytz
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # paginator
from django.http import HttpResponse, Http404
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db import connection
from .decorators import allowed_users , admin_only
from django.contrib.auth.models import Group
from django.db.models import Q
from .queryDashboard import *


def report(request):
    return render(request, 'cases/report_dashboard.html')

def ReportSubProjectOpbkkWeb(request):
    labels = ['ขอ claimcode', 'เข้าระบบไม่ได้', 'ระบบประมวลผล','ระบบรายงาน', 'เพิ่มรหัสสถานพยาบาลใหม่']
    labelOpbkkClient = ['ติดตั้งโปรแกรม', 'ประมวลผลข้อมูล', 'การใช้งานโปรแกรม','เข้าใช้งาน<br>OPBKKClaimClient', 'นำเข้าข้อมูล','ร้องขอข้อมูลล่าสุด','ตรวจสอบข้อมูล','สถานะข้อมูล<br>ไม่ตรงกับหน้าเว็บ','ส่งข้อมูล','UpdatePatch']
    values_m1 = [fnReportOpbkkWeb(44,1), fnReportOpbkkWeb(45,1), fnReportOpbkkWeb(46,1), fnReportOpbkkWeb(47,1), fnReportOpbkkWeb(56,1)]
    values_m2 = [fnReportOpbkkWeb(44,2), fnReportOpbkkWeb(45,2), fnReportOpbkkWeb(46,2), fnReportOpbkkWeb(47,2), fnReportOpbkkWeb(56,2)]
    values_m3 = [fnReportOpbkkWeb(44,3), fnReportOpbkkWeb(45,3), fnReportOpbkkWeb(46,3), fnReportOpbkkWeb(47,3), fnReportOpbkkWeb(56,3)]
    # opbkkclinet
    opbkkclinet_m1 = [fnReportOpbkkWeb(7,1), fnReportOpbkkWeb(8,1), fnReportOpbkkWeb(9,1), fnReportOpbkkWeb(36,1), fnReportOpbkkWeb(37,1),fnReportOpbkkWeb(38,1), fnReportOpbkkWeb(39,1), fnReportOpbkkWeb(40,1), fnReportOpbkkWeb(41,1), fnReportOpbkkWeb(42,1)]
    opbkkclinet_m2 = [fnReportOpbkkWeb(7,2), fnReportOpbkkWeb(8,2), fnReportOpbkkWeb(9,2), fnReportOpbkkWeb(36,2), fnReportOpbkkWeb(37,2),fnReportOpbkkWeb(38,2), fnReportOpbkkWeb(39,2), fnReportOpbkkWeb(40,2), fnReportOpbkkWeb(41,2), fnReportOpbkkWeb(42,2)]
    opbkkclinet_m3 = [fnReportOpbkkWeb(7,3), fnReportOpbkkWeb(8,3), fnReportOpbkkWeb(9,3), fnReportOpbkkWeb(36,3), fnReportOpbkkWeb(37,3),fnReportOpbkkWeb(38,3), fnReportOpbkkWeb(39,3), fnReportOpbkkWeb(40,3), fnReportOpbkkWeb(41,3), fnReportOpbkkWeb(42,3)]
    data = {
        # opbkk-web
            "labels": labels,
            "data_m1": values_m1,
            "data_m2": values_m2,
            "data_m3": values_m3,
            # opbkkclinet
            "labelOpbkkClient":labelOpbkkClient,
            "opbkkclinet_m1": opbkkclinet_m1,
            "opbkkclinet_m2": opbkkclinet_m2,
            "opbkkclinet_m3": opbkkclinet_m3,
        }

    return JsonResponse(data, safe=False)


# def ReportSubProjectOpbkkClient(request):
#     labels = ['ติดตั้งโปรแกรม', 'ประมวลผลข้อมูล', 'การใช้งานโปรแกรม','เข้าใช้งาน<br>OPBKKClaimClient', 'นำเข้าข้อมูล','ร้องขอข้อมูลล่าสุด','ตรวจสอบข้อมูล','สถานะข้อมูล<br>ไม่ตรงกับหน้าเว็บ','ส่งข้อมูล','UpdatePatch']
#     values_m1 = [fnReportOpbkkWeb(7,1), fnReportOpbkkWeb(8,1), fnReportOpbkkWeb(9,1), fnReportOpbkkWeb(36,1), fnReportOpbkkWeb(37,1),fnReportOpbkkWeb(38,1), fnReportOpbkkWeb(39,1), fnReportOpbkkWeb(40,1), fnReportOpbkkWeb(41,1), fnReportOpbkkWeb(42,1)]
#     values_m2 = [fnReportOpbkkWeb(7,2), fnReportOpbkkWeb(8,2), fnReportOpbkkWeb(9,2), fnReportOpbkkWeb(36,2), fnReportOpbkkWeb(37,2),fnReportOpbkkWeb(38,2), fnReportOpbkkWeb(39,2), fnReportOpbkkWeb(40,2), fnReportOpbkkWeb(41,2), fnReportOpbkkWeb(42,2)]
#     values_m3 = [fnReportOpbkkWeb(7,3), fnReportOpbkkWeb(8,3), fnReportOpbkkWeb(9,3), fnReportOpbkkWeb(36,3), fnReportOpbkkWeb(37,3),fnReportOpbkkWeb(38,3), fnReportOpbkkWeb(39,3), fnReportOpbkkWeb(40,3), fnReportOpbkkWeb(41,3), fnReportOpbkkWeb(42,3)]

#     data = {
#         "labels": labels,
#         "data_m1": values_m1,
#         "data_m2": values_m2,
#         "data_m3": values_m3,
#     }
#     return JsonResponse(data, safe=False)
