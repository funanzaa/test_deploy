
import datetime
import pytz
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .filters import HositalFilter

@login_required(login_url='login')
def dashboardPage(request):
    current_user = request.user.id
    case = Case.objects.filter(created_by=current_user).order_by('-id')[:10]
    project = Project.objects.all()
    print(project)
    context = { "all_case": case," all_project": project}
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
    hosptial = Hospitals.objects.get(id=pk)
    form = editHospitalForm()
    form.fields['code'].initial  = hosptial.code
    form.fields['label'].initial  = hosptial.label
    form.fields['h_type'].initial  = hosptial.h_type
    if request.method == 'POST':
        form = editHospitalForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            label = form.cleaned_data["label"]
            h_type = form.cleaned_data["h_type"]
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
                newHospital.save()
                return redirect('hospital-page')
    context = { 'form': form }
    return render(request, 'cases/edit_hospital.html', context)