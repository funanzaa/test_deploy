from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from crm.models import *
import os
import requests
from django.conf import settings
from django.http import HttpResponse, Http404
import json



def HomePage(request):
    return render(request, 'index.html')

def AboutPage(request):
    return render(request,'about.html')

def loginPage(request):

		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('dashboard-page')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}

		return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def model5_dashboard(request):
	# respones_err = requests.get(url_error)
	# res_err = respones_err.json()
	# print(res_err.viewkeys)
	# data = [{'ERR_CODE': '00000', 'ERR_DETAIL': 'เกิดข้อผิดพลาดในระบบ'}
	# print(res_err)
	# lookup_error = model5_lookup_error.objects.all()
	# print(lookup_error)
	url = 'https://bkkapp.nhso.go.th/bkkapp/api/v1/public/HelpdeskReportService/get_total_hosp'
	respones = requests.get(url)
	sum_hosp = respones.json()
	# print(sum_hosp)
	context = {'sum_hosp': sum_hosp}
	return render(request, 'dashboard.html', context)

def hosp_model5(request):
	url = 'https://bkkapp.nhso.go.th/bkkapp/api/v1/public/HelpdeskReportService/get_list_hosp_model5'
	respones = requests.get(url)
	data = respones.json()
	context = {'data': data}
	return render(request, 'hosp_model5.html', context)


from django.db import connection
def lookup_error(request):
	url = 'https://bkkapp.nhso.go.th/bkkapp/api/v1/public/HelpdeskReportService/get_lookup_error'
	respones = requests.get(url)
	x = respones.json()
	y = json.dumps(x)
	jsonDict = json.loads(y)
	count_err = len(jsonDict)
	count_lookup_err = model5_lookup_error.objects.all().count()
	lookup_err = model5_lookup_error.objects.all()
	# print(count_lookup_error)
	if count_lookup_err != count_err:
		lookup_err.delete()
		for i in range(len(jsonDict)):
			err_code = jsonDict[i]['ERR_CODE']
			err_detail = jsonDict[i]['ERR_DETAIL']
			with connection.cursor() as cursor:
				query = "INSERT INTO crm_model5_lookup_error(err_code, err_detail)VALUES('{}','{}');".format(str(err_code),str(err_detail))
				cursor.execute(query)
	context = {'lookup_err':lookup_err}
	return render(request, 'lookup_error.html', context)
