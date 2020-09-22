import datetime
import pytz
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #paginator

@login_required(login_url='login')
def dashboardPage(request):
    current_user = request.user.id
    tz = pytz.timezone('Asia/Bangkok')
    now = (datetime.datetime.now(tz=tz))
    count_hospitals_all = Hospitals.objects.all().count()
    count_project_all = Project.objects.all().count()
    count_case_all = Case.objects.all().count()
    count_case_hos = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=1,date_entered__year=str(now)[:4]).count()
    count_project_opbkk = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=2,date_entered__year=str(now)[:4]).count()
    count_project_erefer = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=3,date_entered__year=str(now)[:4]).count()
    count_project_ehhc = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=4,date_entered__year=str(now)[:4]).count()
    count_project_hshv = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=5,date_entered__year=str(now)[:4]).count()
    count_project_smartcard = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=6,date_entered__year=str(now)[:4]).count()
    count_server = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=7,date_entered__year=str(now)[:4]).count()
    count_other = Case.objects.filter(date_entered__month=str(now)[6:7],project_id=8,date_entered__year=str(now)[:4]).count()
    case = Case.objects.filter(created_by=current_user).order_by('-id')[:10]
    context = {"dates": now ,"all_case": case,"count_hospitals_all":count_hospitals_all,"count_project_all":count_project_all,"count_case_all":count_case_all}
    return render(request, 'cases/dashboard.html',context )

# Add Case
@login_required(login_url='login')
def createCase(request):
    project = Project.objects.all()
    subgroup = Project_subgroup.objects.all()
    service = Service.objects.all()
    hospital = Hospitals.objects.all()
    if request.method == "POST":
        try:
            tz = pytz.timezone('Asia/Bangkok')
            case_name = request.POST.get("name")
            project = request.POST.get("project")
            project_subgroup = request.POST.get("project_subgroup")
            resolution = request.POST.get("resolution")
            service = request.POST.get("service")
            hosptial = request.POST.get("hospital")
            upload_file = request.FILES['case_image']
            newCase = Case()
            newCase.name = case_name
            newCase.project_id = project
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
            return redirect('viewcase')
        except:
            tz = pytz.timezone('Asia/Bangkok')
            case_name = request.POST.get("name")
            project = request.POST.get("project")
            project_subgroup = request.POST.get("project_subgroup")
            resolution = request.POST.get("resolution")
            service = request.POST.get("service")
            hosptial = request.POST.get("hospital")
            newCase = Case()
            newCase.name = case_name
            newCase.project_id = project
            newCase.project_subgroup_id = project_subgroup
            newCase.created_by_id = request.user.id
            newCase.resolution = resolution
            newCase.service_id = service
            newCase.date_entered = datetime.datetime.now(tz=tz)
            newCase.hospitals_id = hosptial
            newCase.save()
            return redirect('viewcase')
    context = {"projects":project,"subgroups":subgroup,"services":service,"hospitals":hospital}
    return render(request, 'cases/add_case.html',context)

#detailCase

def detailCase(request, pk):
    case = Case.objects.get(id=pk)
    context = { 'case': case }
    return render(request, 'cases/detail_case.html', context)

# update Case
def updateCase(request, pk):
    case = Case.objects.get(id=pk)
    project = Project.objects.all()
    subgroup = Project_subgroup.objects.all()
    service = Service.objects.all()
    hospital = Hospitals.objects.all()
    if request.method == "POST":
        try:
            tz = pytz.timezone('Asia/Bangkok')
            case_name = request.POST.get("name")
            project = request.POST.get("project")
            project_subgroup = request.POST.get("project_subgroup")
            resolution = request.POST.get("resolution")
            service = request.POST.get("service")
            hosptial = request.POST.get("hospital")
            upload_file = request.FILES['case_image']
            updateCase = Case.objects.get(id=pk)
            updateCase.name = case_name
            updateCase.project_id = project
            updateCase.project_subgroup_id = project_subgroup
            updateCase.created_by_id = request.user.id
            updateCase.resolution = resolution
            updateCase.service_id = service
            updateCase.update_at = datetime.datetime.now(tz=tz)
            updateCase.hospitals_id = hosptial
            fs = FileSystemStorage()
            name = fs.save(upload_file.name, upload_file)
            url = fs.url(name)
            # print('url:'+ url)
            updateCase.case_pic = url
            updateCase.save()
            return redirect('viewcase')
        except:
            tz = pytz.timezone('Asia/Bangkok')
            case_name = request.POST.get("name")
            project = request.POST.get("project")
            project_subgroup = request.POST.get("project_subgroup")
            resolution = request.POST.get("resolution")
            service = request.POST.get("service")
            hosptial = request.POST.get("hospital")
            updateCase = Case.objects.get(id=pk)
            updateCase.name = case_name
            updateCase.project_id = project
            updateCase.project_subgroup_id = project_subgroup
            updateCase.created_by_id = request.user.id
            updateCase.resolution = resolution
            updateCase.service_id = service
            updateCase.update_at = datetime.datetime.now(tz=tz)
            updateCase.hospitals_id = hosptial
            updateCase.save()
            return redirect('viewcase')
    context = { 'case': case,"projects":project,"subgroups":subgroup,"services":service,"hospitals":hospital }
    return render(request, 'cases/update_case.html', context)

@login_required(login_url='login')
def deleteCase(request, pk):
    case = Case.objects.get(id=pk)
    if request.method == "POST":
        case.delete()
        return redirect('dashboard-page')
    context = {'case': case}
    return render(request, 'cases/delete.html', context)

@login_required(login_url='login')
def hospital(request):
    hospital_list = Hospitals.objects.all().order_by('code')
    page = request.GET.get('page',1)

    paginator = Paginator(hospital_list,10)
    try:
        hospital = paginator.page(page)
    except PageNotAnInteger:
        hospital = paginator.page(page)
    except EmptyPage:
        hospital = paginator.page(paginator.num_pages)
    if request.method == 'GET':
            search_query = request.GET.get('text_find', None)
            if search_query:
                hospital = Hospitals.objects.filter(label__icontains=search_query) | Hospitals.objects.filter(code__icontains=search_query)
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
                    messages.info(request, 'This ' + code +' already')
                elif Label:
                    messages.info(request, 'This ' + label +' already')
                else:
                    newHospital = Hospitals()
                    newHospital.code = code
                    newHospital.label = label
                    newHospital.h_type = h_type
                    tz = pytz.timezone('Asia/Bangkok')
                    newHospital.date_created = datetime.datetime.now(tz=tz)
                    newHospital.save()
                    return redirect('hospital-page')
    context = {'form': form}
    return render(request, 'cases/hospital_form.html', context)

@login_required(login_url='login')
def hospitalEdit(request, pk):
    edithosptial = Hospitals.objects.get(id=pk)
    form = editHospitalForm()
    form.fields['code'].initial  = edithosptial.code
    form.fields['label'].initial  = edithosptial.label
    form.fields['h_type'].initial  = edithosptial.h_type
    if request.method == 'POST':
        form = editHospitalForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            label = form.cleaned_data["label"]
            h_type = form.cleaned_data["h_type"]
            hcode = Hospitals.objects.filter(code=code)
            Label = Hospitals.objects.filter(label=label)
            edithosptial.code = code
            edithosptial.label = label
            edithosptial.h_type = h_type
            edithosptial.save()
            return redirect('hospital-page')
    context = { 'form': form }
    return render(request, 'cases/edit_hospital.html', context)

@login_required(login_url='login')
def create_case_hospital(request, pk):
    hosptial = Hospitals.objects.get(id=pk)
    form = hospitalAddCaseForm()
    if request.method == 'POST':
        form = hospitalAddCaseForm(request.POST,request.FILES)
        if form.is_valid():
            tz = pytz.timezone('Asia/Bangkok')
        try:
            case_name = request.POST['case_name']
            project = request.POST['project']
            project_subgroup = request.POST['project_subgroup']
            resolution = request.POST['resolution']
            service  = request.POST['service']
            upload_file = request.FILES['case_image']
            newCase = Case()
            newCase.name = case_name
            newCase.project_id = project
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
            return redirect('dashboard-page')
        except:
            case_name = request.POST['case_name']
            project = request.POST['project']
            project_subgroup = request.POST['project_subgroup']
            resolution = request.POST['resolution']
            service  = request.POST['service']
            newCase = Case()
            newCase.name = case_name
            newCase.project_id = project
            newCase.project_subgroup_id = project_subgroup
            newCase.created_by_id = request.user.id
            newCase.resolution = resolution
            newCase.service_id = service
            newCase.date_entered = datetime.datetime.now(tz=tz)
            newCase.hospitals_id = hosptial.id
            newCase.save()
            return redirect('dashboard-page')

    context = {'form': form,'hosptial': hosptial}
    return render(request, 'cases/hospital_addcase_form.html', context)

#viewCase
def viewCase(request):
    current_user = request.user.id
    case_list = Case.objects.filter(created_by=current_user).order_by('-id')
    page = request.GET.get('page',1)
    paginator = Paginator(case_list,10)
    try:
        case = paginator.page(page)
    except PageNotAnInteger:
        case = paginator.page(page)
    except EmptyPage:
        case = paginator.page(paginator.num_pages)
    if request.method == 'GET':
            search_query = request.GET.get('text_find', None)
            if search_query:
                case = Case.objects.filter(name__icontains=search_query,created_by=current_user)
                context = {'case': case}
                return render(request, 'cases/case.html', context)
    context = {'case': case}
    return render(request, 'cases/case.html', context)
