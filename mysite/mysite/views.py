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

from django.db.models import Avg, Max, Min, Sum
def model5_dashboard(request):
	# url = 'https://bkkapp.nhso.go.th/bkkapp/api/v1/public/HelpdeskReportService/get_total_hosp'
	# test =  model5_recap_report.objects.all().aggregate(Sum('req_claimcode'))
	with connection.cursor() as cursor:
		url = 'https://bkkapp.nhso.go.th/bkkapp/api/v1/public/HelpdeskReportService/get_total_hosp'
		query = "select sum(req_claimcode::int) from crm_model5_recap_report"
		querySumReqClaim = "select sum(req_claim::int) from crm_model5_recap_report"
		querySumApprove = "select sum(approved::int) from crm_model5_recap_report"
		querySumDenined = "select sum(denined::int) from crm_model5_recap_report"
		cursor.execute(query)
		results = cursor.fetchone()
		cursor.execute(querySumReqClaim)
		resultsReqClaim = cursor.fetchone()
		cursor.execute(querySumApprove)
		resultsApprov = cursor.fetchone()
		cursor.execute(querySumDenined)
		resultsDenined = cursor.fetchone()
		# print(resultsReqClaim[0][0])
		sum_ReqClaimCode  = results[0]
		sum_resultsReqClaim = resultsReqClaim[0]
		sum_Approv  = resultsApprov[0]
		sum_Denined = resultsDenined[0]
		respones = requests.get(url)
		sum_hosp = respones.json()
		# print(sum_hosp)
		# context = {'sum_hosp': sum_hosp,'sum_ReqClaimCode':sum_ReqClaimCode,"sum_resultsReqClaim":resultsReqClaim}
		context = {'sum_hosp': sum_hosp,'sum_ReqClaimCode':sum_ReqClaimCode,"sum_resultsReqClaim":sum_resultsReqClaim,"sum_Approv":sum_Approv,"sum_Denined":sum_Denined}

		print(context)
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



def recepreport(request):
	count_recap_report = model5_recap_report.objects.all().count()
	recap_report = model5_recap_report.objects.all()
	domain = 'https://bkkapp.nhso.go.th/bkkapp/'
	list_hosp = domain + 'api/v1/public/HelpdeskReportService/get_list_hosp_model5'
	total_hosp = 'api/v1/public/HelpdeskReportService/get_total_hosp'
	hcodeAppStatus = 'api/v1/public/HelpdeskReportService/get_hosp_approve_status/' # add hcode
	errCode = 'api/v1/public/HelpdeskReportService/get_error_detail/41666/01003'
	responesListHosp = requests.get(list_hosp)
	jsonListHosp = responesListHosp.json()
	y_jsonListHosp = json.dumps(jsonListHosp)
	jsonDictListHosp = json.loads(y_jsonListHosp)
	if count_recap_report != len(jsonDictListHosp):
		for i in range(len(jsonDictListHosp)):
			hcode = jsonDictListHosp[i]['HSUBOP']
			hname = jsonDictListHosp[i]['HNAME']
			url_hcodeAppStatus = domain + hcodeAppStatus + hcode
			responesHcodeAppStatus= requests.get(url_hcodeAppStatus)
			jsonListHcodeAppStatus = responesHcodeAppStatus.json()
			y_jsonListHcodeAppStatus = json.dumps(jsonListHcodeAppStatus)
			jsonDictHcodeAppStatus = json.loads(y_jsonListHcodeAppStatus)
			req_claimcode = jsonDictHcodeAppStatus[i]['REG_CLAIMCODE']
			req_claim = jsonDictHcodeAppStatus[i]['REG_CLAIM']
			approved = jsonDictHcodeAppStatus[i]['APPROVED']
			denined = jsonDictHcodeAppStatus[i]['DENINED']
			blank = 'blank'
			with connection.cursor() as cursor:
				query = "INSERT INTO crm_model5_recap_report(hcode, hname, req_claimcode, req_claim, approved, denined, err_code) VALUES ('{}', '{}', '{}', '{}', '{}', '{}' ,'{}')".format(hcode,hname,req_claimcode,req_claim,approved,denined,blank)
				cursor.execute(query)
				# recap_report = model5_recap_report.objects.all()
				# context = {"recap_report":recap_report}
				# return render(request, 'recepreport.html', context)
	context = {"recap_report":recap_report}
	return render(request, 'recepreport.html', context)
