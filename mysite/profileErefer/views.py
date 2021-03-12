from django.shortcuts import render
from crm.models import *
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
import datetime
import pytz
from .query import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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
        if checkRequest(hospital) == 0:
            try: # have value profileserver yet
                profile_server = ProfileServer.objects.get(hospitals_id=hospital)
                # print(profile_server)
                newProfileEreferral = ProfileEreferral()
                updateMainHos = Hospitals.objects.get(id=hospital)
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
                # insertProfileErefer(int(profile_server.id),FirstName,LastName,ContactPhone,1,request_date,memo)
                # insertProfileErefer(FirstName,LastName,ContactPhone,1,request_date,memo)
                newProfileServer = ProfileServer()
                newProfileServer.hospitals_id = int(hospital)
                newProfileServer.ContactFirstName = FirstName
                newProfileServer.ContactLastName = LastName
                newProfileServer.ContactPhone = ContactPhone
                newProfileServer.ServerServiceStatus_id = 3 # status recive server
                newProfileServer.save()
                ProfileId = findProfileId(int(hospital))
                updateMainHos = Hospitals.objects.get(id=hospital)
                updateMainHos.main_hospital = hospital_main
                updateMainHos.save()
                newProfileEreferral = ProfileEreferral()
                newProfileEreferral.ProfileServer_id = ProfileId # id profile_server
                newProfileEreferral.ContactFirstName = FirstName
                newProfileEreferral.ContactLastName = LastName
                newProfileEreferral.ContactPhone = ContactPhone
                newProfileEreferral.ServerServiceStatus_id = 1
                newProfileEreferral.request_at = datetime.datetime.now(tz=tz)
                newProfileEreferral.Memo = memo
                newProfileEreferral.save()
                messages.success(request, 'ลงทะเบียนเสร็จสิ้น')
        else:
            messages.error(request, 'พบข้อมูลในระบบแล้ว')
        return HttpResponseRedirect(reverse_lazy('home'))
    context = {"hospital" : hospital,"main_hos" : main_hos}
    return render(request,'profileErefer/requestSetupErefer.html',context)

@login_required(login_url='login')
def SetupErefer(request):
    context = {"ListSetupErefer":ListSetupErefer()
    ,"count_RequestErefer": countRequestErefer()
    ,"ListStatus_user" :  ListStatusCaseErefer(1,request.user.id)
    ,"ListStatus_4" :  ListStatusCaseErefer(4,request.user.id)
    ,"ListStatus_2" :  ListStatusCaseErefer(2,request.user.id)
    ,"user_id" : request.user.id
    }
    return render(request,'profileErefer/SetupErefer.html',context)

@login_required(login_url='login')
def install_Erefer(request,pk):
    os = OperationSystem.objects.all()
    db = database.objects.all()
    web_server = WebServer.objects.all()
    band = ServerBand.objects.all()
    versHosErefer= versHosEreferral.objects.all()
    tz = pytz.timezone('Asia/Bangkok')
    if request.method == "POST":
        os = request.POST.get("os")
        serverband = request.POST.get("serverband")
        db = request.POST.get("db")
        web_server = request.POST.get("web_server")
        ip = request.POST.get("ip")
        dbBackup = request.POST.get("dbBackup")
        versHosErefer = request.POST.get("versHosErefer")
        versErefws = request.POST.get("vers_Erefws")
        testData = request.POST.get("testData")
        testMq = request.POST.get("testMq")
        ereferMemo = request.POST.get("ereferMemo")
        status_case = request.POST.get("status_case")
        # updateupdateProfileServer
        updateProfileServer = ProfileServer.objects.get(id=pk)
        updateProfileServer.OperationSystem_id = os
        updateProfileServer.ServerBand_id = serverband
        updateProfileServer.database_id = db
        updateProfileServer.webServer_id = web_server
        updateProfileServer.FixIpAddress = ip
        updateProfileServer.dbBackup = dbBackup
        updateProfileServer.save()
        update_at = datetime.datetime.now(tz=tz)
        success_at = datetime.datetime.now(tz=tz)
        insert_profileErefer(update_at,success_at,int(status_case),str(request.user.id),int(versErefws),int(versHosErefer),ereferMemo,testData,testMq,int(pk))
        # updateProfileEreferral.save()
        messages.success(request, 'Your ProfileServer is updated successfully!')
        return HttpResponseRedirect(reverse_lazy('profileErefer:SetupErefer'))
    context = {"ListProfile":view_server_profile(pk),"os":os,"db": db
    ,"web_server": web_server,"band":band,"versHosErefer":versHosErefer
    ,"vers_Erefws": ListVersErefws(),"status":ListServerservicestatus()
    ,"count_RequestErefer": countRequestErefer()
    }
    return render(request,'profileErefer/installErefer.html',context)


@login_required(login_url='login')
def setupStatus(request,pk):
    context = {"ListSetupErefer":ListSetupEreferStatus(pk,request.user.id)
    ,"ListStatus_user" :  ListStatusCaseErefer(1,request.user.id)
    ,"ListStatus_4" :  ListStatusCaseErefer(4,request.user.id)
    ,"ListStatus_2" :  ListStatusCaseErefer(2,request.user.id)
    ,"count_RequestErefer": countRequestErefer()
    }
    return render(request,'profileErefer/SetupEreferStatus.html',context)


@login_required(login_url='login')
def updateEreferProfile(request,pk):
    os = OperationSystem.objects.all()
    db = database.objects.all()
    web_server = WebServer.objects.all()
    band = ServerBand.objects.all()
    versHosErefer= versHosEreferral.objects.all()
    tz = pytz.timezone('Asia/Bangkok')
    if request.method == "POST":
        os = request.POST.get("os")
        serverband = request.POST.get("serverband")
        db = request.POST.get("db")
        web_server = request.POST.get("web_server")
        ip = request.POST.get("ip")
        dbBackup = request.POST.get("dbBackup")
        versHosErefer = request.POST.get("versHosErefer")
        versErefws = request.POST.get("vers_Erefws")
        testData = request.POST.get("testData")
        testMq = request.POST.get("testMq")
        ereferMemo = request.POST.get("ereferMemo")
        status_case = request.POST.get("status_case")
        # updateupdateProfileServer
        updateProfileServer = ProfileServer.objects.get(id=pk)
        updateProfileServer.OperationSystem_id = os
        updateProfileServer.ServerBand_id = serverband
        updateProfileServer.database_id = db
        updateProfileServer.webServer_id = web_server
        updateProfileServer.FixIpAddress = ip
        updateProfileServer.dbBackup = dbBackup
        updateProfileServer.save()
        update_at = datetime.datetime.now(tz=tz)
        update_profileErefer(update_at,int(status_case),str(request.user.id),int(versErefws),int(versHosErefer),ereferMemo,testData,testMq,int(pk))
        messages.success(request, 'Your ProfileServer is updated successfully!')
        return HttpResponseRedirect(reverse_lazy('profileErefer:SetupErefer'))
    context = {"ListProfile":view_server_profile(pk),"os":os,"db": db
    ,"web_server": web_server,"band":band,"versHosErefer":versHosErefer
    ,"vers_Erefws": ListVersErefws(),"status":ListServerservicestatus()
    ,"count_RequestErefer": countRequestErefer()
    }
    return render(request,'profileErefer/updateEreferProfile.html',context)

@login_required(login_url='login')
def check_case_lock(request):
    if request.method == 'GET':
        try:
            tz = pytz.timezone('Asia/Bangkok')
            profile_id = request.GET["ProfileServer_id"]
            updateProfileEreferral = ProfileEreferral.objects.get(ProfileServer_id=profile_id)
            # print(profile_id)
            updateProfileEreferral.case_locking = '1'
            updateProfileEreferral.case_staff_lock = request.user.id
            updateProfileEreferral.case_lock_date_time = datetime.datetime.now(tz=tz)
            updateProfileEreferral.save()
        except:
            pass
        return HttpResponse("ok")


def OverAllHc(request):
    context = {"ListOverAllHc":ListOverAllHc()
    ,"ListStatus_user" :  ListStatusCaseErefer(1,request.user.id)
    ,"ListStatus_4" :  ListStatusCaseErefer(4,request.user.id)
    ,"ListStatus_2" :  ListStatusCaseErefer(2,request.user.id)
    }
    return render(request,'profileErefer/OverAllHc.html',context)
