import datetime
import pytz
# import os
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # paginator
from django.http import HttpResponse
import json
# from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db import connection
from .decorators import allowed_users , admin_only
# from django.contrib.auth.models import Group
from django.db.models import Q
from django.core.files.storage import default_storage # delete file

from .queryDashboard import *


@login_required(login_url='login')
# @allowed_users(allowed_roles=['helpdesk','programmer']) # permission
# @admin_only
def dashboardPage(request):

    current_user = request.user.id
    tz = pytz.timezone('Asia/Bangkok')
    now = (datetime.datetime.now(tz=tz))
    count_hospital = Hospitals.objects.filter(h_type=1).count()
    count_hc = Hospitals.objects.filter(h_type=3).count()
    count_clinic = Hospitals.objects.filter(h_type=4).count()
    count_project_all = Project.objects.all().count()
    count_case_all = Case.objects.all().count()
    count_case_hos = queryProjectAll("HospitalOS",now.month)
    count_case_opbkk = queryProjectAll("OPBKKClaim-Client",now.month)
    count_case_erefer = queryProjectAll("E-referral",now.month)
    count_case_ehhc = queryProjectAll("eHHC",now.month)
    count_case_hshv = queryProjectAll("HSHV",now.month)
    count_case_smartcard = queryProjectAll("SmartCard",now.month)
    count_case_server = queryProjectAll("Server",now.month)
    count_case_other = queryProjectAll("ประชาชน",now.month)
    count_case_bkkApp = queryProjectAll("BkkApp",now.month)
    count_case_eClaim = queryProjectAll("E-claim",now.month)
    count_case_hosAdmin = queryProjectAll("HospitalOS-Admin",now.month)
    count_case_hosReport = queryProjectAll("HospitalOS-Report",now.month)
    count_case_opbkkWeb = queryProjectAll("OPBKKClaim - Web",now.month)
    count_case_bppds = queryProjectAll("BPPDS",now.month)
    count_case_ktb = queryProjectAll("กรุงไทย APP",now.month)

    count_case_total = Case.objects.filter(date_entered__month=now.month).count()
    count_call = Case.objects.filter(date_entered__month=now.month, service_id=1).count()
    count_line = Case.objects.filter(date_entered__month=now.month, service_id=2).count()
    count_facebook = Case.objects.filter(date_entered__month=now.month, service_id=3).count()
    count_email = Case.objects.filter(date_entered__month=now.month, service_id=4).count()
    count_Line_official = Case.objects.filter(date_entered__month=now.month, service_id=5).count()
    context = {
        "dates": now, "count_hospital": count_hospital, "count_hc": count_hc, "count_clinic": count_clinic,
        "count_project_all": count_project_all, "count_case_all": count_case_all, "count_case_hos": count_case_hos, "count_case_opbkk": count_case_opbkk,
        "count_case_erefer": count_case_erefer, "count_case_ehhc": count_case_ehhc, "count_case_hshv": count_case_hshv, "count_case_smartcard": count_case_smartcard,
        "count_case_bkkapp": count_case_bkkApp,"count_case_eClaim": count_case_eClaim,"count_case_hosAdmin": count_case_hosAdmin,"count_case_hosReport": count_case_hosReport,
        "count_case_opbkkWeb": count_case_opbkkWeb,"count_case_bppds": count_case_bppds,"count_case_ktb": count_case_ktb,
        "count_case_server": count_case_server, "count_case_other": count_case_other, "count_case_total": count_case_total,
        "count_call": count_call, "count_line": count_line, "count_facebook": count_facebook, "count_email": count_email, "count_Line_official": count_Line_official,
        "count_RequestErefer": countRequestErefer()
        ,"count_SetupErefer_11722":deshboardSetupEreferral(11722),"count_SetupErefer_11482":deshboardSetupEreferral(11482),"count_SetupErefer_11470":deshboardSetupEreferral(11470)
        ,"count_SetupErefer_11478":deshboardSetupEreferral(11478)
    }
    return render(request, 'cases/dashboard.html', context)

# Add Case


@login_required(login_url='login')
def createCase(request):
    project = Project.objects.all()
    statusCase = StatusCase.objects.all()
    staff  = User.objects.filter(~Q(id = request.user.id )).filter(~Q(username = 'admin' )).filter(~Q(is_active = False ))
    service = Service.objects.all()
    hospital = Hospitals.objects.all()
    if request.method == "POST":
        chkAssign = request.POST.get("chkAssign")
        if chkAssign == 'yes':
            try:
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                project_subgroup = request.POST.get("locality") # subgroup Project
                resolution = request.POST.get("resolution")
                service = request.POST.get("service")
                hosptial = request.POST.get("hospital")
                priority   = request.POST.get("priority")
                chkAssign = request.POST.get("chkAssign")
                userAssign = request.POST.get("locality-assign")
                upload_file = request.FILES['case_image']
                newCase = Case()
                newCase.name = case_name
                newCase.project_subgroup_id = project_subgroup
                newCase.created_by_id = int(userAssign)
                newCase.resolution = resolution
                newCase.service_id = service
                newCase.date_entered = datetime.datetime.now(tz=tz)
                newCase.hospitals_id = hosptial
                newCase.assign = chkAssign
                newCase.assign_at = datetime.datetime.now(tz=tz)
                newCase.assign_by = request.user.id
                newCase.priorityCase = priority
                fs = FileSystemStorage()
                name = fs.save(upload_file.name, upload_file)
                url = fs.url(name)
                newCase.case_pic = url
                newCase.save()
                messages.success(request, 'Your case is added successfully!')
                return HttpResponseRedirect(reverse_lazy('viewcase'))
            except:
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                chkAssign = request.POST.get("chkAssign")
                userAssign = request.POST.get("locality-assign")
                project_subgroup = request.POST.get("locality")
                resolution = request.POST.get("resolution")
                service = request.POST.get("service")
                hosptial = request.POST.get("hospital")
                priority   = request.POST.get("priority")
                newCase = Case()
                newCase.name = case_name
                newCase.project_subgroup_id = project_subgroup
                newCase.created_by_id = int(userAssign)
                newCase.resolution = resolution
                newCase.service_id = service
                newCase.date_entered = datetime.datetime.now(tz=tz)
                newCase.hospitals_id = hosptial
                newCase.assign = chkAssign
                newCase.assign_at = datetime.datetime.now(tz=tz)
                newCase.assign_by = request.user.id

                newCase.priorityCase = priority
                
                newCase.save()
                messages.success(request, 'Your case is added successfully!')
                return HttpResponseRedirect(reverse_lazy('viewcase'))
        else:
            try:
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                #project = request.POST.get("project")  Cancal save
                project_subgroup = request.POST.get("locality") # subgroup Project
                # project("project_subgroup" + str(project_subgroup))
                resolution = request.POST.get("resolution")
                service = request.POST.get("service")
                hosptial = request.POST.get("hospital")
                upload_file = request.FILES['case_image']
                newCase = Case()
                newCase.name = case_name
                # newCase.project_id = project
                newCase.project_subgroup_id = project_subgroup
                newCase.created_by_id = request.user.id
                newCase.resolution = resolution
                newCase.service_id = service
                newCase.date_entered = datetime.datetime.now(tz=tz)
                newCase.hospitals_id = hosptial
                fs = FileSystemStorage()
                name = fs.save(upload_file.name, upload_file)
                url = fs.url(name)
                # print('url:'+ url)
                newCase.case_pic = url
                newCase.save()
                messages.success(request, 'Your case is added successfully!')
                return HttpResponseRedirect(reverse_lazy('viewcase'))
            except:
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                # project = request.POST.get("project") cancal
                # project_subgroup = request.POST.get("project_subgroup")
                project_subgroup = request.POST.get("locality")
                resolution = request.POST.get("resolution")
                service = request.POST.get("service")
                hosptial = request.POST.get("hospital")
                # print(chkAssign)
                newCase = Case()
                newCase.name = case_name
                # newCase.project_id = project
                newCase.project_subgroup_id = project_subgroup
                newCase.created_by_id = request.user.id
                newCase.resolution = resolution
                newCase.service_id = service
                newCase.date_entered = datetime.datetime.now(tz=tz)
                newCase.hospitals_id = hosptial
                newCase.save()
                messages.success(request, 'Your case is added successfully!')
                return HttpResponseRedirect(reverse_lazy('viewcase'))
        
    context = {"projects": project,
               "services": service, "hospitals": hospital,"statusCases":statusCase,"staffs":staff}
    return render(request, 'cases/add_case.html', context)

# detailCaseAssign

def detailCaseAssign(request, pk):
    case = Case.objects.get(id=pk)
    context = {'case': case}
    return render(request, 'cases/detailCaseAssign.html', context)


# detailCase



def detailCase(request, pk):
    case = Case.objects.get(id=pk)
    context = {'case': case}
    return render(request, 'cases/detail_case.html', context)

# update Case


def updateCase(request, pk):
    case = Case.objects.get(id=pk)
    project = Project.objects.all()
    subgroup = Project_subgroup.objects.all()
    service = Service.objects.all()
    hospital = Hospitals.objects.all()
    statusCase = StatusCase.objects.all()
    staff  = User.objects.filter(~Q(id = request.user.id )).filter(~Q(username = 'admin' )).filter(~Q(is_active = False ))
    if request.method == "POST":
        chkAssign = request.POST.get("chkAssign")
        status_assign = request.POST.get("status_assign")
        if chkAssign == 'yes': # case forward
            try:
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                # project = request.POST.get("project2")
                project_subgroup = request.POST.get("localityUpdate")
                resolution = request.POST.get("solution")
                service = request.POST.get("service")
                hosptial = request.POST.get("hospital")
                statusCase = request.POST.get("statusCase")
                staff   = request.POST.get("locality-assign")

                priority   = request.POST.get("priority")
                # priority2   = request.POST.get("priority2")

                upload_file = request.FILES['case_image']
                updateCase = Case.objects.get(id=pk)
                updateCase.name = case_name
                # updateCase.project_id = project
                updateCase.project_subgroup_id = project_subgroup
                updateCase.created_by_id = staff
                updateCase.resolution = resolution
                updateCase.service_id = service
                updateCase.update_at = datetime.datetime.now(tz=tz)
                updateCase.hospitals_id = hosptial
                updateCase.status_Case_id = ''
                updateCase.statusCaseUpdate_at = datetime.datetime.now(tz=tz)
                fs = FileSystemStorage()
                name = fs.save(upload_file.name, upload_file)
                url = fs.url(name)
                updateCase.priorityCase = priority
                updateCase.case_pic = url
                updateCase.save()
                messages.success(request, 'Your case is updated successfully!')
                return HttpResponseRedirect(reverse_lazy('viewcase'))
            except:
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                project_subgroup = request.POST.get("localityUpdate")
                resolution = request.POST.get("solution")
                service = request.POST.get("service")
                hosptial = request.POST.get("hospital")
                statusCase = request.POST.get("statusCase")
                staff   = request.POST.get("locality-assign")
                priority   = request.POST.get("priority")
                updateCase = Case.objects.get(id=pk)
                updateCase.name = case_name
                updateCase.project_subgroup_id = project_subgroup
                updateCase.created_by_id = staff
                updateCase.forward_by = request.user.id # forward by
                updateCase.resolution = resolution
                updateCase.service_id = service
                updateCase.update_at = datetime.datetime.now(tz=tz)
                updateCase.hospitals_id = hosptial
                updateCase.status_Case_id = ''
                updateCase.statusCaseUpdate_at = datetime.datetime.now(tz=tz)
                updateCase.assign_at = datetime.datetime.now(tz=tz)
                updateCase.forward_at = datetime.datetime.now(tz=tz)
                updateCase.priorityCase = priority
                updateCase.save()
                messages.success(request, 'Your case is updated successfully!')
                return HttpResponseRedirect(reverse_lazy('viewcase'))
        elif status_assign == 'yes':
            try:
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                project_subgroup = request.POST.get("localityUpdate")

                _resolution = request.POST.get("solution")
                _solution = request.POST.get("ass_resolution")

                service = request.POST.get("service")
                hosptial = request.POST.get("hospital")
                statusCase = request.POST.get("statusCase")
                upload_file = request.FILES['case_image']
                updateCase = Case.objects.get(id=pk)
                updateCase.name = case_name
                updateCase.project_subgroup_id = project_subgroup
                updateCase.created_by_id = request.user.id

                updateCase.resolution = _resolution
                updateCase.solution= _solution

                updateCase.service_id = service
                updateCase.update_at = datetime.datetime.now(tz=tz)
                updateCase.hospitals_id = hosptial
                updateCase.status_Case_id = statusCase
                updateCase.statusCaseUpdate_at = datetime.datetime.now(tz=tz)
                fs = FileSystemStorage()
                name = fs.save(upload_file.name, upload_file)
                url = fs.url(name)
                updateCase.case_pic = url
                updateCase.save()
                messages.success(request, 'Your case is updated successfully!')
                return HttpResponseRedirect(reverse_lazy('viewcase'))
            except:
                # print(status_assign)
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                project_subgroup = request.POST.get("localityUpdate")

                _resolution = request.POST.get("solution")
                _solution = request.POST.get("ass_resolution")

                service = request.POST.get("service")
                hosptial = request.POST.get("hospital")
                statusCase = request.POST.get("statusCase")
                request_id = request.user.id
                updateCase = Case.objects.get(id=pk)
                updateCase.name = case_name
                updateCase.project_subgroup_id = project_subgroup
                updateCase.created_by_id = request.user.id

                updateCase.resolution = _resolution
                updateCase.solution= _solution

                updateCase.service_id = service
                updateCase.update_at = datetime.datetime.now(tz=tz)
                updateCase.hospitals_id = hosptial
                updateCase.status_Case_id = statusCase
                updateCase.statusCaseUpdate_at = datetime.datetime.now(tz=tz)
                updateCase.save()
                messages.success(request, 'Your case is updated successfully!')
                return HttpResponseRedirect(reverse_lazy('viewcase'))
        else:
            try:
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                project_subgroup = request.POST.get("localityUpdate")

                resolution = request.POST.get("resolution")
                # resolution = request.POST.get("resolution")

                service = request.POST.get("service")
                hosptial = request.POST.get("hospital")
                statusCase = request.POST.get("statusCase")
                upload_file = request.FILES['case_image']
                updateCase = Case.objects.get(id=pk)
                updateCase.name = case_name
                updateCase.project_subgroup_id = project_subgroup
                updateCase.created_by_id = request.user.id
                updateCase.resolution = resolution
                updateCase.service_id = service
                updateCase.update_at = datetime.datetime.now(tz=tz)
                updateCase.hospitals_id = hosptial
                updateCase.status_Case_id = statusCase
                updateCase.statusCaseUpdate_at = datetime.datetime.now(tz=tz)
                fs = FileSystemStorage()
                name = fs.save(upload_file.name, upload_file)
                url = fs.url(name)
                updateCase.case_pic = url
                updateCase.save()
                messages.success(request, 'Your case is updated successfully!')
                return HttpResponseRedirect(reverse_lazy('viewcase'))
            except:
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                project_subgroup = request.POST.get("localityUpdate")

                resolution = request.POST.get("solution")
                resolution = request.POST.get("resolution")

                service = request.POST.get("service")
                hosptial = request.POST.get("hospital")
                statusCase = request.POST.get("statusCase")
                request_id = request.user.id
                updateCase = Case.objects.get(id=pk)
                updateCase.name = case_name
                updateCase.project_subgroup_id = project_subgroup
                updateCase.created_by_id = request.user.id
                updateCase.resolution = resolution
                updateCase.service_id = service
                updateCase.update_at = datetime.datetime.now(tz=tz)
                updateCase.hospitals_id = hosptial
                updateCase.status_Case_id = statusCase
                updateCase.statusCaseUpdate_at = datetime.datetime.now(tz=tz)
                updateCase.save()
                messages.success(request, 'Your case is updated successfully!')
                return HttpResponseRedirect(reverse_lazy('viewcase'))
    context = {'case': case, "projects": project, "subgroups": subgroup,
               "services": service, "hospitals": hospital,"statusCases":statusCase,"staffs":staff}
    return render(request, 'cases/update_case.html', context)


@login_required(login_url='login')
def deleteCase(request, pk):
    case = Case.objects.get(id=pk)
    if request.method == "POST":
        case.delete()
        messages.success(request, 'Your case is deleted successfully!')
        return HttpResponseRedirect(reverse_lazy('viewcase'))
    context = {'case': case}
    return render(request, 'cases/delete.html', context)


@login_required(login_url='login')
def hospital(request):
    hospital_list = Hospitals.objects.all().order_by('code')
    page = request.GET.get('page', 1)

    paginator = Paginator(hospital_list, 30)
    try:
        hospital = paginator.page(page)
    except PageNotAnInteger:
        hospital = paginator.page(page)
    except EmptyPage:
        hospital = paginator.page(paginator.num_pages)
    if request.method == 'GET':
        search_query = request.GET.get('text_find', None)
        if search_query:
            hospital = Hospitals.objects.filter(
                label__icontains=search_query) | Hospitals.objects.filter(code__icontains=search_query)
            context = {'hospital': hospital}
            return render(request, 'cases/hospital.html', context)
    context = {'hospital': hospital,"count_RequestErefer": countRequestErefer()}
    return render(request, 'cases/hospital.html', context)


@login_required(login_url='login')
def hospitalAdd(request):
    form = hospitalForm()
    if request.method == 'POST':
        form = hospitalForm(request.POST)
        if form.is_valid():
            code = request.POST['code']
            label = request.POST['label']
            h_type = request.POST['h_type']
            hcode = Hospitals.objects.filter(code=code)
            Label = Hospitals.objects.filter(label=label)
            if hcode:
                messages.info(request, 'This ' + code + ' already')
            elif Label:
                messages.info(request, 'This ' + label + ' already')
            else:
                newHospital = Hospitals()
                newHospital.code = code
                newHospital.label = label
                newHospital.h_type = h_type
                tz = pytz.timezone('Asia/Bangkok')
                newHospital.date_created = datetime.datetime.now(tz=tz)
                newHospital.save()
                messages.success(request, 'Your hospital is added successfully!')
                return HttpResponseRedirect(reverse_lazy('hospital-page'))
    context = {'form': form}
    return render(request, 'cases/hospital_form.html', context)


@login_required(login_url='login')
def hospitalEdit(request, pk):
    edithosptial = Hospitals.objects.get(id=pk)
    form = editHospitalForm()
    form.fields['code'].initial = edithosptial.code
    form.fields['label'].initial = edithosptial.label
    form.fields['h_type'].initial = edithosptial.h_type
    form.fields['active'].initial = edithosptial.active
    form.fields['install_app'].initial = edithosptial.install_app
    form.fields['training'].initial = edithosptial.training
    if request.method == 'POST':
        form = editHospitalForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            label = form.cleaned_data["label"]
            h_type = form.cleaned_data["h_type"]
            active = form.cleaned_data["active"]
            install_app = form.cleaned_data["install_app"]
            training = form.cleaned_data["training"]
            hcode = Hospitals.objects.filter(code=code)
            Label = Hospitals.objects.filter(label=label)
            edithosptial.code = code
            edithosptial.label = label
            edithosptial.h_type = h_type
            edithosptial.active = active
            edithosptial.install_app = install_app
            edithosptial.training = training
            edithosptial.save()
            messages.success(request, 'Your hospital is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('hospital-page'))
    context = {'form': form}
    return render(request, 'cases/edit_hospital.html', context)


@login_required(login_url='login')
def create_case_hospital(request, pk):
    hosptial = Hospitals.objects.get(id=pk)
    project = Project.objects.all()
    subgroup = Project_subgroup.objects.all()
    service = Service.objects.all()
    if request.method == 'POST':
        try:
            tz = pytz.timezone('Asia/Bangkok')
            case_name = request.POST['name']
            # project = request.POST['project']
            project_subgroup = request.POST['locality-hospital']
            resolution = request.POST['resolution']
            service = request.POST['service']
            upload_file = request.FILES['case_image']
            newCase = Case()
            newCase.name = case_name
            # newCase.project_id = project
            newCase.project_subgroup_id = project_subgroup
            newCase.created_by_id = request.user.id
            newCase.resolution = resolution
            newCase.service_id = service
            newCase.date_entered = datetime.datetime.now(tz=tz)
            newCase.hospitals_id = hosptial.id
            fs = FileSystemStorage()
            name = fs.save(upload_file.name, upload_file)
            url = fs.url(name)
            newCase.case_pic = url
            newCase.save()
            messages.success(request, 'Your case is added successfully!')
            return HttpResponseRedirect(reverse_lazy('viewcase'))
        except:
            case_name = request.POST['name']
            # project = request.POST['project']
            project_subgroup = request.POST['locality-hospital']
            resolution = request.POST['resolution']
            service = request.POST['service']
            newCase = Case()
            newCase.name = case_name
            # newCase.project_id = project
            newCase.project_subgroup_id = project_subgroup
            newCase.created_by_id = request.user.id
            newCase.resolution = resolution
            newCase.service_id = service
            newCase.date_entered = datetime.datetime.now(tz=tz)
            newCase.hospitals_id = hosptial.id
            newCase.save()
            messages.success(request, 'Your case is added successfully!')
            return HttpResponseRedirect(reverse_lazy('viewcase'))

    context = {'projects': project, 'subgroups': subgroup,
               'services': service, 'hosptial': hosptial}
    return render(request, 'cases/hospital_addcase_form.html', context)

# viewCase

@login_required(login_url='login')
def viewCase(request):
    tz = pytz.timezone('Asia/Bangkok')
    now = (datetime.datetime.now(tz=tz))
    user = User.objects.all()
    current_user = request.user.id
    # case = Case.objects.filter(created_by=current_user)
    if len(str(now)[5:7]) == 2:
        # case = Case.objects.filter(created_by=current_user)
        case = Case.objects.filter(date_entered__month=str(now)[5:7], created_by=current_user, date_entered__year=str(now)[:4])
    else:
        # case = Case.objects.filter(created_by=current_user)
        case = count_case_hos = Case.objects.filter(date_entered__month=str(now)[6:7], created_by=current_user, date_entered__year=str(now)[:4])

    countAssignSend = Case.objects.filter(assign_by=str(current_user)).count()
    countAssignForward = Case.objects.filter(forward_by=str(current_user)).count()
    countAssign = countAssignSend + countAssignForward
    context = {'case': case,'users':user,'countAssigns': countAssign,"count_RequestErefer": countRequestErefer()}
    return render(request, 'cases/case.html', context)

@login_required(login_url='login')
def viewCaseAssign(request):
    user = User.objects.all()
    current_user = request.user.id
    case = Case.objects.filter(assign_by=str(current_user)) | Case.objects.filter(forward_by=str(current_user))
    countAssignSend = Case.objects.filter(assign_by=str(current_user)).count()
    countAssignForward = Case.objects.filter(forward_by=str(current_user)).count()
    countAssign = countAssignSend + countAssignForward
    context = {'case': case,'users':user,'countAssigns': countAssign}
    return render(request, 'cases/viewCaseAssign.html', context)


from django.db import connection

@login_required(login_url='login')
def controlversions(request):
    with connection.cursor() as cursor:
        query = """
        select  CONCAT(cc."app_controlVersion", ' | ', cc."hos_s_version") AS "app_controlVersion",
        CONCAT(cc."hos_stock_version", ' | ', cc."hos_ereferral_version") AS "app_hosVersion"
        ,ch.label 
        ,cc.date_created 
        ,cc.hcode 
        FROM crm_controlversion cc
        left join crm_hospitals ch on cc.hcode = ch.code
        where cc.hcode not in ('sql fail')
        order by date_created desc;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        x = cursor.description
        resultsList = []  
        for r in results:
            i = 0
            d = {}
            while i < len(x):
                d[x[i][0]] = r[i]
                i = i+1
            resultsList.append(d)
        context = {'ControlVersion': resultsList,"count_RequestErefer": countRequestErefer()}
        return render(request, 'cases/crontrol_version.html', context)


from rest_framework.views import APIView  # rest_framework
from rest_framework.response import Response  # rest_framework
from rest_framework.authtoken.views import ObtainAuthToken  # rest_framework
from rest_framework.authtoken.models import Token  # rest_framework
from rest_framework import status
from .serializers import *


# List_Subproject
@login_required(login_url='login')
def List_Subproject(request, pk):
    subgroup = Project_subgroup.objects.filter(project=pk).values('id', 'name')
    list_subgroup = json.dumps(list(subgroup))
    # print(list_subgroup)
    return HttpResponse(list_subgroup)

# Profile Server

def Profile_Server(request):
    hospital = Hospitals.objects.filter(~Q(code = '00000')).order_by('code')
    serverband = ServerBand.objects.all()
    if request.method == "POST":
        _hosptial = request.POST.get("hospital")
        if checkRequestServerDup(_hosptial) == 0:
            try:
                tz = pytz.timezone('Asia/Bangkok')
                hosptial = request.POST.get("hospital")
                serverBand = request.POST.get("serverband")
                firstName = request.POST.get("FirstName")
                lastName = request.POST.get("LastName")
                contactPhone = request.POST.get("ContactPhone")
                contactEmail = request.POST.get("ContactEmail")
                radioUseServer = request.POST.get("radioUseServer")
                _memo = request.POST.get("memo")
                upload_file = request.FILES['case_image']
                fs = FileSystemStorage()
                name = fs.save(upload_file.name, upload_file)
                url = fs.url(name)
                # datetimeSendServer = datetime.datetime.now(tz=tz)
                newProfileServer = ProfileServer()
                newProfileServer.hospitals_id = hosptial
                newProfileServer.ServerBand_id = serverBand
                newProfileServer.ContactFirstName = firstName
                newProfileServer.ContactLastName = lastName
                newProfileServer.ContactPhone = contactPhone
                newProfileServer.ContactEmail = contactEmail
                newProfileServer.UseServer = radioUseServer
                newProfileServer.Memo = _memo
                newProfileServer.ServerServiceStatus_id = 1 # status recive server
                newProfileServer.datetimeSendServer = datetime.datetime.now(tz=tz)
                newProfileServer.ServerImage = url
                newProfileServer.save()
                messages.success(request, 'รับเข้าระบบแล้ว')
                return HttpResponseRedirect(reverse_lazy('home'))
            except:
                tz = pytz.timezone('Asia/Bangkok')
                hosptial = request.POST.get("hospital")
                serverBand = request.POST.get("serverband")
                firstName = request.POST.get("FirstName")
                lastName = request.POST.get("LastName")
                contactPhone = request.POST.get("ContactPhone")
                contactEmail = request.POST.get("ContactEmail")
                radioUseServer = request.POST.get("radioUseServer")
                _memo = request.POST.get("memo")
                # datetimeSendServer = datetime.datetime.now(tz=tz)
                newProfileServer = ProfileServer()
                newProfileServer.hospitals_id = hosptial
                newProfileServer.ServerBand_id = serverBand
                newProfileServer.ContactFirstName = firstName
                newProfileServer.ContactLastName = lastName
                newProfileServer.ContactPhone = contactPhone
                newProfileServer.ContactEmail = contactEmail
                newProfileServer.UseServer = radioUseServer
                newProfileServer.Memo = _memo
                newProfileServer.ServerServiceStatus_id = 1 # status recive server
                newProfileServer.datetimeSendServer = datetime.datetime.now(tz=tz)
                newProfileServer.save()
                messages.success(request, 'รับเข้าระบบแล้ว')
                return HttpResponseRedirect(reverse_lazy('home'))
        else:
            messages.error(request, 'พบรหัสสถานพยาบาลนี้ซ้ำในระบบ')
            return HttpResponseRedirect(reverse_lazy('home'))
    context = {"hospitals": hospital,"serverbands":serverband,"count_RequestErefer": countRequestErefer()}
    return render(request, 'cases/ProfileServer.html', context)

@login_required(login_url='login')
def ListAllProfileServer(request):
    ProfileServers = ProfileServer.objects.all().order_by('id')
    countProfileServers1 = ProfileServer.objects.filter(ServerServiceStatus_id=1).count()
    countProfileServers2 = ProfileServer.objects.filter(ServerServiceStatus_id=2).count()
    countProfileServers3 = ProfileServer.objects.filter(ServerServiceStatus_id=3).count()
    context = {"ProfileServer":ProfileServers,
    "countProfileServers1":countProfileServers1,
    "countProfileServers2":countProfileServers2,
    "countProfileServers3":countProfileServers3
    ,"count_RequestErefer": countRequestErefer()}
    return render(request, 'cases/ListAllProfileServer.html', context)

@login_required(login_url='login')
def ListProfileServer(request,pk):
    ProfileServers = ProfileServer.objects.filter(ServerServiceStatus_id=pk).order_by('id')
    countProfileServers1 = ProfileServer.objects.filter(ServerServiceStatus_id=1).count()
    countProfileServers2 = ProfileServer.objects.filter(ServerServiceStatus_id=2).count()
    countProfileServers3 = ProfileServer.objects.filter(ServerServiceStatus_id=3).count()
    context = {"ProfileServer":ProfileServers,
    "countProfileServers1":countProfileServers1,
    "countProfileServers2":countProfileServers2,
    "countProfileServers3":countProfileServers3,
    "count_RequestErefer": countRequestErefer()}
    return render(request, 'cases/ListProfileServer.html', context)


@login_required(login_url='login')
def SetupServer(request,pk):
    ProfileServers = ProfileServer.objects.get(id=pk)
    ProfileServerslist = ProfileServer.objects.filter(id=pk)
    OperationSystems = OperationSystem.objects.all()
    databases = database.objects.all()
    WebServers = WebServer.objects.all()
    if request.method == "POST":
        tz = pytz.timezone('Asia/Bangkok')
        os = request.POST.get("os")
        ip = request.POST.get("ip")
        db = request.POST.get("database")
        webserver = request.POST.get("webserver")
        backupdbd = request.POST.get("backupdb")
        _memo = request.POST.get("memo")
        ProfileServers = ProfileServer.objects.get(id=pk)
        ProfileServers.OperationSystem_id = os
        ProfileServers.FixIpAddress = ip
        ProfileServers.database_id = db
        ProfileServers.webServer_id = webserver
        ProfileServers.dbBackup = backupdbd
        ProfileServers.Memo = _memo
        ProfileServers.datetimeCompleteServer = datetime.datetime.now(tz=tz)
        ProfileServers.ServerServiceStatus_id = 2
        ProfileServers.created_by_id = request.user.id
        # print(ProfileServers.hospitals_id)
        ProfileServers.save()
        newCase = Case()
        newCase.name = "ติดตั้ง Server (เข้าระบบ)"
        newCase.project_subgroup_id = 14
        newCase.created_by_id = request.user.id
        newCase.resolution = "ติดตั้ง Server (เข้าระบบ)"
        newCase.service_id = 6
        newCase.date_entered = datetime.datetime.now(tz=tz)
        newCase.hospitals_id = ProfileServers.hospitals_id
        newCase.save()
        return HttpResponseRedirect(reverse_lazy('ListAllProfileServer'))
        # updateProfileServers
    # print(ProfileServerslist)
    context = {"OperationSystem":OperationSystems,"database":databases,
    "WebServer":WebServers,"ProfileServerslists":ProfileServerslist}
    return render(request, 'cases/SetupServer.html', context)


def receiveServer(request):
    context = {}
    if request.method == "POST":
        search_hcode = request.POST.get('table_search')
        with connection.cursor() as cursor:
            cursor.execute(""" 
            select crm_ProfileServer.id as pro_id,h.code,h.label ,crm_serverservicestatus.id,crm_serverservicestatus."name" ,crm_ProfileServer."datetimeSendServer" ,crm_ProfileServer."datetimeReceiveServer" ,crm_ProfileServer."datetimeCompleteServer",crm_ProfileServer."Memo" 
            from crm_ProfileServer
            inner join crm_hospitals h ON crm_ProfileServer.hospitals_id = h.id 
            inner join crm_serverservicestatus on crm_ProfileServer."ServerServiceStatus_id" = crm_serverservicestatus.id 
                where h.code = %(hcode)s
            """, {'hcode': search_hcode})
            results = cursor.fetchall()
            x = cursor.description
            resultsList = []  
            for r in results:
                i = 0
                d = {}
                while i < len(x):
                    d[x[i][0]] = r[i]
                    i = i+1
                resultsList.append(d)
        context = {'resultsLists': resultsList}
    # print(context)
    return render(request, 'cases/receiveServer.html', context)



def userReceiveServer(request,pk):
    tz = pytz.timezone('Asia/Bangkok')
    ProfileServers = ProfileServer.objects.get(id=pk)
    ProfileServers.ServerServiceStatus_id = 3
    ProfileServers.datetimeReceiveServer = datetime.datetime.now(tz=tz)
    ProfileServers.save()
    messages.success(request, 'ยืนยันรับเครื่อง')
    return HttpResponseRedirect(reverse_lazy('home'))



@login_required(login_url='login')
def editProfileServer(request,pk):
    profile_server = ProfileServer.objects.get(id=pk)
    os = OperationSystem.objects.all()
    db = database.objects.all()
    web_server = WebServer.objects.all()
    band = ServerBand.objects.all()
    if request.method == "POST":
        tz = pytz.timezone('Asia/Bangkok')
        _os = request.POST.get("os")
        serverband = request.POST.get("serverband")
        postgres_version = request.POST.get("db")
        webServer = request.POST.get("web_server")
        ip_address = request.POST.get("ip")
        db_Backup = request.POST.get("dbBackup")
        UseServer = request.POST.get("radioUseServer")
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        contact_phone = request.POST.get("ContactPhone")
        contact_email = request.POST.get("ContactEmail")
        memo = request.POST.get("memo")
        try:
            upload_file = request.FILES['case_image']
            updateProfileServer = ProfileServer.objects.get(id=pk)
            name_file =  updateProfileServer.ServerImage
            substring_namefile =  str(name_file)[7:]
            BASE_DIR = settings.MEDIA_ROOT
            path_file = BASE_DIR + "\\" + substring_namefile # path file del test windows
            default_storage.delete(path_file)
            fs = FileSystemStorage()
            name = fs.save(upload_file.name, upload_file)
            url = fs.url(name)
            updateProfileServer.ServerImage = url
            updateProfileServer.OperationSystem_id = _os
            updateProfileServer.ServerBand_id = serverband
            updateProfileServer.database_id = postgres_version
            updateProfileServer.webServer_id = webServer
            updateProfileServer.FixIpAddress = ip_address
            updateProfileServer.dbBackup = db_Backup
            updateProfileServer.UseServer = UseServer
            updateProfileServer.ContactFirstName = firstName
            updateProfileServer.ContactLastName = lastName
            updateProfileServer.ContactPhone = contact_phone
            updateProfileServer.ContactEmail = contact_email
            updateProfileServer.Memo = memo
            updateProfileServer.update_by = request.user.id
            updateProfileServer.update_at = datetime.datetime.now(tz=tz)
            updateProfileServer.save()
            messages.success(request, 'Your ProfileServer is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('ListAllProfileServer'))
        except:
            updateProfileServer = ProfileServer.objects.get(id=pk)
            updateProfileServer.OperationSystem_id = _os
            updateProfileServer.ServerBand_id = serverband
            updateProfileServer.database_id = postgres_version
            updateProfileServer.webServer_id = webServer
            updateProfileServer.FixIpAddress = ip_address
            updateProfileServer.dbBackup = db_Backup
            updateProfileServer.UseServer = UseServer
            updateProfileServer.ContactFirstName = firstName
            updateProfileServer.ContactLastName = lastName
            updateProfileServer.ContactPhone = contact_phone
            updateProfileServer.ContactEmail = contact_email
            updateProfileServer.Memo = memo
            updateProfileServer.update_by = request.user.id
            updateProfileServer.update_at = datetime.datetime.now(tz=tz)
            updateProfileServer.save()
            messages.success(request, 'Your ProfileServer is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('ListAllProfileServer'))
    context = {"profile_server": profile_server,"os":os,"db": db
    ,"web_server": web_server,"band":band}
    # print(context)
    return render(request, 'cases/editProfileServer.html', context)


@login_required(login_url='login')
def detailServerProfile(request,pk):
    ProfileServers = ProfileServer.objects.get(id=pk)
    context = {"ProfileServer":ProfileServers}
    return render(request, 'cases/detailServerProfile.html', context)

def userDetailServerProfile(request,pk):
    ProfileServers = ProfileServer.objects.get(id=pk)
    context = {"ProfileServer":ProfileServers}
    return render(request, 'cases/userDetailServerProfile.html', context)

@login_required(login_url='login')
def AssignMonitor(request):
    with connection.cursor() as cursor:
        cursor.execute(""" 
        select ROW_NUMBER () OVER (ORDER BY auth_user.first_name) as rowNumber
        ,auth_user.id as userId
        ,auth_user.first_name,auth_user.last_name
        ,sum(case when crm_case."status_Case_id" is null then 1 else 0 end) as status_assign
        ,(((sum(case when crm_case."status_Case_id" is null then 1 else 0 end)) * 100 )::real / (sum(case when crm_case."status_Case_id" is null then 1 else 0 end) + sum(case when crm_case."status_Case_id" = 1 then 1 else 0 end) + sum(case when crm_case."status_Case_id" = 5 then 1 else 0 end)))::numeric(5,2)as percent_status_assign
        ,sum(case when crm_case."status_Case_id" = 1 then 1 else 0 end) as status_close
        ,((sum(case when crm_case."status_Case_id" = 1 then 1 else 0 end) * 100 )::real / (sum(case when crm_case."status_Case_id" is null then 1 else 0 end) + sum(case when crm_case."status_Case_id" = 1 then 1 else 0 end) + sum(case when crm_case."status_Case_id" = 5 then 1 else 0 end)))::numeric(5,2) as percent_status_close
        ,sum(case when crm_case."status_Case_id" = 5 then 1 else 0 end) as status_pending
        ,((sum(case when crm_case."status_Case_id" = 5 then 1 else 0 end)*100)::real / (sum(case when crm_case."status_Case_id" is null then 1 else 0 end) + sum(case when crm_case."status_Case_id" = 1 then 1 else 0 end) + sum(case when crm_case."status_Case_id" = 5 then 1 else 0 end)))::numeric(5,2) as percent_status_pending
        ,(sum(case when crm_case."status_Case_id" is null then 1 else 0 end) + sum(case when crm_case."status_Case_id" = 1 then 1 else 0 end) + sum(case when crm_case."status_Case_id" = 5 then 1 else 0 end)) as total_case
        ,sum(case when (crm_case."status_Case_id" is null and crm_case."priorityCase" = '1'  ) then 1 else 0 end) as check_urgent
        ,sum(case when (crm_case."status_Case_id" is null and crm_case."priorityCase" = '2'  ) then 1 else 0 end) as check_very_urgent
        ,sum(case when (crm_case."status_Case_id" = 5 and crm_case."priorityCase" = '1'  ) then 1 else 0 end) as check_status_pending_urgent
        ,sum(case when (crm_case."status_Case_id" = 5 and crm_case."priorityCase" = '2'  ) then 1 else 0 end) as check_status_pending_very_urgent
        from crm_case
        inner join auth_user ON crm_case.created_by_id = auth_user.id
        where crm_case.assign = 'yes'
        group by userId,auth_user.first_name,auth_user.last_name
                """)
        results = cursor.fetchall()
        x = cursor.description
        resultsList = []  
        for r in results:
            i = 0
            d = {}
            while i < len(x):
                d[x[i][0]] = r[i]
                i = i+1
            resultsList.append(d)
        context = {'resultsLists': resultsList}
    return render(request, 'cases/assignMonitor.html', context)


# Monitor Case

@login_required(login_url='login')
def monitorStatusAssignCase(request,pk):
    case = Case.objects.filter(created_by=int(pk)).filter(status_Case_id=None)
    context = {'case': case}
    return render(request, 'cases/monitorStatusAssignCase.html', context)

@login_required(login_url='login')
def monitorStatusPendingCase(request,pk):
    case = Case.objects.filter(created_by=int(pk)).filter(status_Case_id=5)
    context = {'case': case}
    return render(request, 'cases/monitorStatusPendingCase.html', context)

@login_required(login_url='login')
def monitorStatusCloseCase(request,pk):
    case = Case.objects.filter(created_by=int(pk)).filter(status_Case_id=1)
    context = {'case': case}
    return render(request, 'cases/monitorStatusCloseCase.html', context)

# End  Monitor Case