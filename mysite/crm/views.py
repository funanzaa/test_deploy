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
    count_case_hos = Case.objects.filter(date_entered__month=now.month, project_id=1).count()
    count_case_opbkk = Case.objects.filter(date_entered__month=now.month, project_id=2).count()
    count_case_erefer = Case.objects.filter(date_entered__month=now.month, project_id=3).count()
    count_case_ehhc = Case.objects.filter(date_entered__month=now.month, project_id=4).count()
    count_case_hshv = Case.objects.filter(date_entered__month=now.month, project_id=5).count()
    count_case_smartcard = Case.objects.filter(date_entered__month=now.month, project_id=6).count()
    count_case_server = Case.objects.filter(date_entered__month=now.month, project_id=7).count()
    count_case_other = Case.objects.filter(date_entered__month=now.month, project_id=8).count()
    count_case_total = Case.objects.filter(date_entered__month=now.month).count()
    count_call = Case.objects.filter(date_entered__month=now.month, service_id=1).count()
    count_line = Case.objects.filter(date_entered__month=now.month, service_id=2).count()
    count_facebook = Case.objects.filter(date_entered__month=now.month, service_id=3).count()
    count_email = Case.objects.filter(date_entered__month=now.month, service_id=4).count()
    count_Line_official = Case.objects.filter(date_entered__month=now.month, service_id=5).count()
    # sub setup
    count_sub_hos = Case.objects.filter(
        date_entered__month=now.month, project_id=1, project_subgroup_id=1).count()
    count_sub_opbkk = Case.objects.filter(
        date_entered__month=now.month, project_id=2, project_subgroup_id=1).count()
    count_sub_erefer = Case.objects.filter(
        date_entered__month=now.month, project_id=3, project_subgroup_id=1).count()
    count_sub_ehhc = Case.objects.filter(
        date_entered__month=now.month, project_id=4, project_subgroup_id=1).count()
    count_sub_hshv = Case.objects.filter(
        date_entered__month=now.month, project_id=5, project_subgroup_id=1).count()
    count_sub_smartcard = Case.objects.filter(
        date_entered__month=now.month, project_id=6, project_subgroup_id=1).count()
    count_sub_server = Case.objects.filter(
        date_entered__month=now.month, project_id=7, project_subgroup_id=1).count()
    # sub use program
    count_use_sub_hos = Case.objects.filter(
        date_entered__month=now.month, project_id=1, project_subgroup_id=3).count()
    count_use_sub_opbkk = Case.objects.filter(
        date_entered__month=now.month, project_id=2, project_subgroup_id=3).count()
    count_use_sub_erefer = Case.objects.filter(
        date_entered__month=now.month, project_id=3, project_subgroup_id=3).count()
    count_use_sub_ehhc = Case.objects.filter(
        date_entered__month=now.month, project_id=4, project_subgroup_id=3).count()
    count_use_sub_hshv = Case.objects.filter(
        date_entered__month=now.month, project_id=5, project_subgroup_id=3).count()
    count_use_sub_smartcard = Case.objects.filter(
        date_entered__month=now.month, project_id=6, project_subgroup_id=3).count()
    count_use_sub_server = Case.objects.filter(
        date_entered__month=now.month, project_id=7, project_subgroup_id=3).count()
    # sub process
    count_process_sub_hos = Case.objects.filter(
        date_entered__month=now.month, project_id=1, project_subgroup_id=2).count()
    count_process_sub_opbkk = Case.objects.filter(
        date_entered__month=now.month, project_id=2, project_subgroup_id=2).count()
    count_process_sub_erefer = Case.objects.filter(
        date_entered__month=now.month, project_id=3, project_subgroup_id=2).count()
    count_process_sub_ehhc = Case.objects.filter(
        date_entered__month=now.month, project_id=4, project_subgroup_id=2).count()
    count_process_sub_hshv = Case.objects.filter(
        date_entered__month=now.month, project_id=5, project_subgroup_id=2).count()
    count_process_sub_smartcard = Case.objects.filter(
        date_entered__month=now.month, project_id=6, project_subgroup_id=2).count()
    count_process_sub_server = Case.objects.filter(
        date_entered__month=now.month, project_id=7, project_subgroup_id=2).count()

    context = {
        "dates": now, "count_hospital": count_hospital, "count_hc": count_hc, "count_clinic": count_clinic,
        "count_project_all": count_project_all, "count_case_all": count_case_all, "count_case_hos": count_case_hos, "count_case_opbkk": count_case_opbkk,
        "count_case_erefer": count_case_erefer, "count_case_ehhc": count_case_ehhc, "count_case_hshv": count_case_hshv, "count_case_smartcard": count_case_smartcard,
        "count_case_server": count_case_server, "count_case_other": count_case_other, "count_case_total": count_case_total,
        "count_call": count_call, "count_line": count_line, "count_facebook": count_facebook, "count_email": count_email, "count_Line_official": count_Line_official,
        "count_sub_hos": count_sub_hos, "count_sub_opbkk": count_sub_opbkk, "count_sub_erefer": count_sub_erefer, "count_sub_ehhc": count_sub_ehhc, "count_sub_hshv": count_sub_hshv, "count_sub_smartcard": count_sub_smartcard, "count_sub_server": count_sub_server,
        "count_use_sub_hos": count_use_sub_hos, "count_use_sub_opbkk": count_use_sub_opbkk, "count_use_sub_erefer": count_use_sub_erefer, "count_use_sub_ehhc": count_use_sub_ehhc, "count_use_sub_hshv": count_use_sub_hshv, "count_use_sub_smartcard": count_use_sub_smartcard, "count_use_sub_server": count_use_sub_server,
        "count_process_sub_hos": count_process_sub_hos, "count_process_sub_opbkk": count_process_sub_opbkk, "count_process_sub_erefer": count_process_sub_erefer, "count_process_sub_ehhc": count_process_sub_ehhc, "count_process_sub_hshv": count_process_sub_hshv, "count_process_sub_smartcard": count_process_sub_smartcard, "count_process_sub_server": count_process_sub_server

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

def fnUpdateCaseAssign(pk,tz,case_name,project_subgroup,resolution,service,hosptial,statusCase,staff,request_id):
    updateCase = Case.objects.get(id=pk)
    updateCase.name = case_name
    updateCase.project_subgroup_id = project_subgroup
    print('staff : ' + str(staff))
    updateCase.created_by_id = staff
    updateCase.assign_by = request_id
    updateCase.resolution = resolution
    updateCase.service_id = service
    updateCase.update_at = datetime.datetime.now(tz=tz)
    updateCase.hospitals_id = hosptial 
    updateCase.status_Case_id = None
    updateCase.statusCaseUpdate_at = datetime.datetime.now(tz=tz)
    updateCase.save()
    # messages.success( 'Your case is updated successfully!')
    return HttpResponseRedirect(reverse_lazy('viewcase'))

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
        if chkAssign == 'yes':
            try:
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                # project = request.POST.get("project2")
                project_subgroup = request.POST.get("localityUpdate")
                resolution = request.POST.get("resolution")
                service = request.POST.get("service")
                hosptial = request.POST.get("hospital")
                statusCase = request.POST.get("statusCase")
                upload_file = request.FILES['case_image']
                updateCase = Case.objects.get(id=pk)
                updateCase.name = case_name
                # updateCase.project_id = project
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
                # print('url:'+ url)
                updateCase.case_pic = url
                updateCase.save()
                messages.success(request, 'Your case is updated successfully!')
                return HttpResponseRedirect(reverse_lazy('viewcase'))
            except:
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                project_subgroup = request.POST.get("localityUpdate")
                resolution = request.POST.get("resolution")
                service = request.POST.get("service")
                hosptial = request.POST.get("hospital")
                statusCase = request.POST.get("statusCase")
                staff   = request.POST.get("locality-assign")
                # if assignYes == 'yes':
                #     fnUpdateCaseAssign(pk,tz,case_name,project_subgroup,resolution,service,hosptial,statusCase,staff,request_id)
                updateCase = Case.objects.get(id=pk)
                updateCase.name = case_name
                updateCase.project_subgroup_id = project_subgroup
                updateCase.created_by_id = staff
                updateCase.assign_by = request.user.id
                updateCase.resolution = resolution
                updateCase.service_id = service
                updateCase.update_at = datetime.datetime.now(tz=tz)
                updateCase.hospitals_id = hosptial
                updateCase.status_Case_id = ''
                # updateCase.statusCaseUpdate_at = datetime.datetime.now(tz=tz)
                updateCase.assign_at = datetime.datetime.now(tz=tz)
                updateCase.save()
                messages.success(request, 'Your case is updated successfully!')
                return HttpResponseRedirect(reverse_lazy('viewcase'))
        else:
            try:
                tz = pytz.timezone('Asia/Bangkok')
                case_name = request.POST.get("name")
                project_subgroup = request.POST.get("localityUpdate")
                resolution = request.POST.get("resolution")
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
    context = {'hospital': hospital}
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
    user = User.objects.all()
    current_user = request.user.id
    case = Case.objects.filter(created_by=current_user)
    countAssign = Case.objects.filter(assign_by=str(current_user)).count()
    context = {'case': case,'users':user,'countAssigns': countAssign}
    return render(request, 'cases/case.html', context)

@login_required(login_url='login')
def viewCaseAssign(request):
    user = User.objects.all()
    current_user = request.user.id
    case = Case.objects.filter(assign_by=str(current_user))
    countAssign = Case.objects.filter(assign_by=str(current_user)).count()
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
        context = {'ControlVersion': resultsList}
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
    hospital = Hospitals.objects.filter(h_type=4)
    serverband = ServerBand.objects.all()
    if request.method == "POST":
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
    context = {"hospitals": hospital,"serverbands":serverband}
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
    "countProfileServers3":countProfileServers3}
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
    "countProfileServers3":countProfileServers3}
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
def detailServerProfile(request,pk):
    ProfileServers = ProfileServer.objects.get(id=pk)
    context = {"ProfileServer":ProfileServers}
    return render(request, 'cases/detailServerProfile.html', context)

def userDetailServerProfile(request,pk):
    ProfileServers = ProfileServer.objects.get(id=pk)
    context = {"ProfileServer":ProfileServers}
    return render(request, 'cases/userDetailServerProfile.html', context)


