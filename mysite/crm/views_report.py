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


def report(request):
    project = Project.objects.all()
    if request.method == "POST":
        
        dateTime = request.POST.get("date")
        project = request.POST.get("project")
        print(dateTime)
        print(project)

    context = {"projects":project}
    return render(request, 'cases/report_dashboard.html', context)