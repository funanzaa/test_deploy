import datetime
import pytz
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboardPage(request):
    current_user = request.user.id
    count_case_hos = Case.objects.filter(project_id=1).count()
    count_project_opbkk = Case.objects.filter(project_id=2).count()
    count_project_erefer = Case.objects.filter(project_id=3).count()
    count_project_ehhc = Case.objects.filter(project_id=4).count()
    count_project_hshv = Case.objects.filter(project_id=5).count()
    count_project_smartcard = Case.objects.filter(project_id=6).count()
    case = Case.objects.filter(created_by=current_user).order_by('-id')[:10]
    context = {'count_smartcard':count_project_smartcard,'count_hshv':count_project_hshv,'count_ehhc':count_project_ehhc,'count_erefer' : count_project_erefer,'count_opbkk': count_project_opbkk,'count_hos': count_case_hos, "all_case": case}
    return render(request, 'cases/dashboard.html',context )


@login_required(login_url='login')
def createCase(request):
    form = CaseForm()
    if request.method == 'POST':
        # print('Printing POST: ', request.POST)
        form = CaseForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            tz = pytz.timezone('Asia/Bangkok')
            obj.date_entered = datetime.datetime.now(tz=tz)
            try:
                obj.created_by = request.user
                upload_file = request.FILES['case_pic']
                fs = FileSystemStorage()
                name = fs.save(upload_file.name, upload_file)
                url = fs.url(name)
                obj.case_pic = url
            # print(upload_file.name)
            # print(upload_file.size)
                obj.save()
                return redirect('dashboard-page')
            except:
                obj.created_by = request.user
                form.save()
                return redirect('dashboard-page')
    context = {'form': form}
    return render(request, 'cases/case_form.html', context)

@login_required(login_url='login')
def updateCase(request, pk):
    case = Case.objects.get(id=pk)
    form = updateCaseForm(instance=case)

    if request.method == 'POST':
        form = updateCaseForm(request.POST, instance=case)
        if form.is_valid():
            obj = form.save(commit=False)
            tz = pytz.timezone('Asia/Bangkok')
            try:
                obj.created_by = request.user
                obj.update_at = datetime.datetime.now(tz=tz)
                upload_file = request.FILES['case_pic']
                fs = FileSystemStorage()
                name = fs.save(upload_file.name, upload_file)
                url = fs.url(name)
                obj.case_pic = url
            # print(upload_file.name)
            # print(upload_file.size)
                obj.save()
                return redirect('dashboard-page')
            except:
                obj.update_at = datetime.datetime.now(tz=tz)
                obj.created_by = request.user
                form.save()
                return redirect('dashboard-page')

    context = { 'form': form }
    return render(request, 'cases/case_form.html', context)

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
    if request.method == 'GET':
            search_query = request.GET.get('text_find', None)
            if search_query:
                hospital = Hospitals.objects.filter(label__icontains=search_query) | Hospitals.objects.filter(code__icontains=search_query)
                context = {'hospital': hospital}
                return render(request, 'cases/hospital.html', context)
    return render(request, 'cases/hospital.html')

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