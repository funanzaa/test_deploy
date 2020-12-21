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
import datetime 
import pytz
from datetime import timedelta
from django.db.models import Avg, Max, Min, Sum


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

from django.db.models import Q
def model5_dashboard(request):
	with connection.cursor() as cursor:
		recap_report = model5_recap_report.objects.all()
		count_installApp = Hospitals.objects.filter(install_app='Yes').count()
		count_training = Hospitals.objects.filter(training='Yes').count()
		countHospReqClaim = model5_recap_report.objects.filter(~Q(req_claimcode='0')).count()
		countHospSendClaim = model5_recap_report.objects.filter(~Q(req_claim='0')).count()
		max_date = model5_recap_report.objects.latest("date_created").date_created
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
		sum_ReqClaimCode  = "{:,}".format(results[0])
		sum_resultsReqClaim = "{:,}".format(resultsReqClaim[0])
		sum_Approv  = "{:,}".format(resultsApprov[0])
		sum_Denined = "{:,}".format(resultsDenined[0])
		respones = requests.get(url)
		sum_hosp = respones.json()
		# print(count_installApp)
		context = {'sum_hosp': sum_hosp,'sum_ReqClaimCode':sum_ReqClaimCode,"sum_resultsReqClaim":sum_resultsReqClaim,
		"sum_Approv":sum_Approv,"sum_Denined":sum_Denined,"max_date":max_date,"count_installApp":count_installApp,
		"count_training":count_training,"countHospReqClaim":countHospReqClaim,"countHospSendClaim":countHospSendClaim}
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
	try:
		recap_report = model5_recap_report.objects.all()
		max_date = model5_recap_report.objects.latest("date_created").date_created
		domain = 'https://bkkapp.nhso.go.th/bkkapp/'
		list_hosp = domain + 'api/v1/public/HelpdeskReportService/get_list_hosp_model5'
		# total_hosp = 'api/v1/public/HelpdeskReportService/get_total_hosp'
		hcodeAppStatus = 'api/v1/public/HelpdeskReportService/get_hosp_approve_status/' # add hcode ex.'api/v1/public/HelpdeskReportService/get_error_detail/41666/01003'
		responesListHosp = requests.get(list_hosp)
		url_hcodeAppStatus = list_hosp
		jsonListHosp = responesListHosp.json()
		y_jsonListHosp = json.dumps(jsonListHosp)
		jsonDictListHosp = json.loads(y_jsonListHosp)
		tz = pytz.timezone('Asia/Bangkok')
		date_current = datetime.datetime.now(tz=tz)
		if int(date_current.day) == int(max_date.strftime("%d")): 
			context = {"recap_report":recap_report}
			return render(request, 'recepreport.html', context)
		else:
			recap_report.delete() # delete data on table
			for i in range(len(jsonDictListHosp)):
				hcode = jsonDictListHosp[i]['HSUBOP']
				hname = jsonDictListHosp[i]['HNAME']
				url_hcodeAppStatus = domain + hcodeAppStatus + hcode
				responesHcodeAppStatus= requests.get(url_hcodeAppStatus)
				jsonListHcodeAppStatus = responesHcodeAppStatus.json()
				req_claimcode = jsonListHcodeAppStatus[0]['REG_CLAIMCODE']
				req_claim = jsonListHcodeAppStatus[0]['REG_CLAIM']
				approved = jsonListHcodeAppStatus[0]['APPROVED']
				denined = jsonListHcodeAppStatus[0]['DENINED']
				blank = 'blank'
				date_created = date_current
				with connection.cursor() as cursor:
					query = "INSERT INTO crm_model5_recap_report(hcode, hname, req_claimcode, req_claim, approved, denined, err_code , date_created) VALUES ('{}', '{}', '{}', '{}', '{}', '{}' ,'{}','{}')".format(hcode,hname,req_claimcode,req_claim,approved,denined,blank,date_created)
					cursor.execute(query)
			context = {"recap_report":recap_report}
	except:
		context = {"recap_report":recap_report}
	return render(request, 'recepreport.html', context)


def installApp(request):
	hosInstallApp = Hospitals.objects.filter(install_app='Yes')
	context = {"hosInstallApp":hosInstallApp}
	return render(request, 'installApp.html', context)

def training(request):
	hosTraining = Hospitals.objects.filter(training='Yes')
	context = {"hosInstallApp":hosTraining}
	return render(request, 'training.html', context)



def amountHospReqClaimcode(request):
	amountHospReqClaimcode = model5_recap_report.objects.filter(~Q(req_claimcode='0'))
	context = {"amountHospReqClaimcode":amountHospReqClaimcode}
	return render(request, 'amountHospReqClaimcode.html', context)

def amountHospReqClaim(request):
	amountHospReqClaim = model5_recap_report.objects.filter(~Q(req_claim='0'))
	context = {"amountHospReqClaim":amountHospReqClaim}
	return render(request, 'amountHospReqClaim.html', context)


def amountDataHospReqClaimCode(request):
	amountDataHospReqClaimCode = model5_recap_report.objects.filter(~Q(req_claimcode='0'))
	context = {"amountDataHospReqClaimCode":amountDataHospReqClaimCode}
	return render(request, 'amountDataHospReqClaimCode.html', context)


def amountDataHospReqClaim(request):
	amountDataHospReqClaim = model5_recap_report.objects.filter(~Q(req_claim='0'))
	context = {"amountDataHospReqClaim":amountDataHospReqClaim}
	return render(request, 'amountDataHospReqClaim.html', context)

def HospApprove(request):
	HospApprove = model5_recap_report.objects.filter(~Q(req_claim='0'))
	context = {"HospApprove":HospApprove}
	return render(request, 'HospApprove.html', context)



def fnInsertErrDetaill(err_code,total_denined,hcode,err_detail,date_current):
	with connection.cursor() as cursor:
		query = "INSERT INTO public.crm_error_detail(hcode, err_code, err_detail, total_denined, date_created)VALUES ( '{}', '{}', '{}', '{}','{}');".format(hcode,err_code,err_detail,total_denined,date_current)
		cursor.execute(query)

def ErrorDetail(request):
	try:
		errDetail = error_detail.objects.all()
		max_date = error_detail.objects.latest("date_created").date_created
		url = 'https://bkkapp.nhso.go.th/bkkapp/api/v1/public/HelpdeskReportService/get_error_detail'
		tz = pytz.timezone('Asia/Bangkok')
		date_current = datetime.datetime.now(tz=tz)
		responesDetailErr= requests.get(url)
		jsonresponesDetailErr = responesDetailErr.json()
	 	# ex.{'ERR_CODE': '00008', 'TOTAL_DENINED': '33', 'HCODE': '41757', 'ERR_DETAIL': 'การวินิจฉัยโรค ไม่อยู่ในเงื่อนไขการบริการผู้ป่วยนอก'}
		if int(date_current.day) == int(max_date.strftime("%d")):
			with connection.cursor() as cursor:
				query_sumErr = """
	 					select t1.hcode,t1.hname,sum(total) as total
	 					from (select r.hcode,r.hname,sum(total_denined::int) as total
	 						from crm_error_detail e
	 						inner join crm_model5_recap_report r on r.hcode::int  = e.hcode::int
	 						group by r.hcode,r.hname,e.total_denined ) t1
	 					group by t1.hcode,t1.hname
	 				"""
				cursor.execute(query_sumErr)
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
			context = {'resultsList': resultsList}
			return render(request, 'ErrorDetail.html', context)
		else:
			errDetail.delete()
			for i in range(len(jsonresponesDetailErr)):
				err_code = jsonresponesDetailErr[i]['ERR_CODE']
				total_denined = jsonresponesDetailErr[i]['TOTAL_DENINED']
				hcode = jsonresponesDetailErr[i]['HCODE']
				err_detail = jsonresponesDetailErr[i]['ERR_DETAIL']
				fnInsertErrDetaill(err_code,total_denined,hcode,err_detail,date_current)
		query_sumErr = """
			select t1.hcode,t1.hname,sum(total) as total
			from (select r.hcode,r.hname,sum(total_denined::int) as total
				from crm_error_detail e
				inner join crm_model5_recap_report r on r.hcode::int  = e.hcode::int
				--where e.hcode = '41687'
				group by r.hcode,r.hname,e.total_denined ) t1
			group by t1.hcode,t1.hname
		"""
		with connection.cursor() as cursor:
			cursor.execute(query_sumErr)
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
		context = {'resultsList': resultsList}
		return render(request, 'ErrorDetail.html', context)
	except:
		context = {}
		return render(request, 'ErrorDetail.html', context)

	

def ErrorDetailHcode(request,hcode):
	with connection.cursor() as cursor:
		cursor.execute(""" select err_code,err_detail,sum(total_denined::int)
            from crm_error_detail
            where hcode = %(hcode)s
			group by err_code,err_detail
         """, {'hcode': hcode})
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
	context = {'resultsList': resultsList}
	return render(request,'ErrorDetailHcode.html',context)