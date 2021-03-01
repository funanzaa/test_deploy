from django.shortcuts import render
from crm.models import *
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
import datetime
import pytz
from .query import *

def requestSetupErefer(request):
    hospital = Hospitals.objects.all()
    main_hos = main_hospital.objects.all()
    if request.method == "POST":
        hospital = request.POST.get("hospital")
        FirstName = request.POST.get("FirstName")
        LastName = request.POST.get("LastName")
        ContactPhone = request.POST.get("ContactPhone")
        hospital_main = request.POST.get("hospital_main")
        memo = request.POST.get("memo")
        tz = pytz.timezone('Asia/Bangkok')
        # print(checkRequest(hospital))
        if checkRequest(hospital) == 0:
            try: # have value profileserver yet
                profile_server = ProfileServer.objects.get(hospitals_id=hospital)
                updateMainHos = Hospitals.objects.get(id=hospital)
                newProfileEreferral = ProfileEreferral()
                newProfileEreferral.ProfileServer_id = profile_server.id # id profile_server
                newProfileEreferral.ContactFirstName = FirstName
                newProfileEreferral.ContactLastName = LastName
                newProfileEreferral.ContactPhone = ContactPhone
                newProfileEreferral.ServerServiceStatus_id = 1
                newProfileEreferral.request_at = datetime.datetime.now(tz=tz)
                newProfileEreferral.Memo = memo
                newProfileEreferral.save()
                updateMainHos.main_hospital = hospital_main
                updateMainHos.save()
                messages.success(request, 'ลงทะเบียนเสร็จสิ้น')
            except: # not value profileserver yet
                # add table ProfileServer
                newProfileServer = ProfileServer()
                newProfileServer.hospitals_id = hospital
                newProfileServer.ContactFirstName = FirstName
                newProfileServer.ContactLastName = LastName
                newProfileServer.ContactPhone = ContactPhone
                newProfileServer.ServerServiceStatus_id = 3 # status recive server
                newProfileServer.save()
                profile_server = ProfileServer.objects.get(hospitals_id=hospital)
                updateMainHos = Hospitals.objects.get(id=hospital)
                newProfileEreferral = ProfileEreferral()
                newProfileEreferral.ProfileServer_id = profile_server.id # id profile_server
                newProfileEreferral.ContactFirstName = FirstName
                newProfileEreferral.ContactLastName = LastName
                newProfileEreferral.ContactPhone = ContactPhone
                newProfileEreferral.ServerServiceStatus_id = 1
                newProfileEreferral.request_at = datetime.datetime.now(tz=tz)
                newProfileEreferral.Memo = memo
                newProfileEreferral.save()
                updateMainHos.main_hospital = hospital_main
                updateMainHos.save()
                messages.success(request, 'ลงทะเบียนเสร็จสิ้น')
        else:
            messages.error(request, 'พบข้อมูลในระบบแล้ว')
        # messages.success(request, 'ลงทะเบียนเสร็จสิ้น')
        return HttpResponseRedirect(reverse_lazy('home'))
    context = {"hospital" : hospital,"main_hos" : main_hos}
    return render(request,'profileErefer/requestSetupErefer.html',context)


def SetupErefer(request):
    context = {"ListSetupErefer":ListSetupErefer()}
    return render(request,'profileErefer/SetupErefer.html',context)

def install_Erefer(request,pk):
    os = OperationSystem.objects.all()
    db = database.objects.all()
    web_server = WebServer.objects.all()
    band = ServerBand.objects.all()
    versHosErefer= versHosEreferral.objects.all()
    vers_Erefws = versErefws.objects.all()
    context = {"ListProfile":view_server_profile(pk),
    "os":os,"db": db,"web_server": web_server,"band":band,"versHosErefer":versHosErefer,"vers_Erefws":vers_Erefws
    }
    return render(request,'profileErefer/installErefer.html',context)
