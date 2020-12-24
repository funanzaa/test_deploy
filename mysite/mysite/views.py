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
from django.views.generic import View
from rest_framework.views import APIView  # rest_framework
from rest_framework.response import Response  # rest_framework


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

	try:
		timeperiod = datatimeperiod.objects.all()
		recap_report = model5_recap_report.objects.all()
		max_date = model5_recap_report.objects.latest("date_created").date_created
		domain = 'https://bkkapp.nhso.go.th/bkkapp/'
		list_hosp = domain + 'api/v1/public/HelpdeskReportService/get_list_hosp_model5'
		hcodeAppStatus = 'api/v1/public/HelpdeskReportService/get_hosp_approve_status/'
		apiTimeperiod = 'api/v1/public/DataService/query/Time_period'
		responesListHosp = requests.get(list_hosp)
		url_hcodeAppStatus = list_hosp
		jsonListHosp = responesListHosp.json()
		y_jsonListHosp = json.dumps(jsonListHosp)
		jsonDictListHosp = json.loads(y_jsonListHosp)
		tz = pytz.timezone('Asia/Bangkok')
		date_current = datetime.datetime.now(tz=tz)
		if int(date_current.day) != int(max_date.strftime("%d")): #insert data
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
				dataknow = jsonListHcodeAppStatus[0]['REG_CLAIMCODE_ADDNONCC']
				date_created = date_current
				FnRecapReport(hcode,hname,req_claimcode,req_claim,approved,denined,dataknow,date_created)
			CreateTimePeriod()
		with connection.cursor() as cursor:
			recap_report = model5_recap_report.objects.all()
			count_hosp = model5_recap_report.objects.all().count()
			count_installApp = Hospitals.objects.filter(install_app='Yes').count()
			count_training = Hospitals.objects.filter(training='Yes').count()
			countHospReqClaim = model5_recap_report.objects.filter(~Q(req_claimcode='0')).count()
			max_date = model5_recap_report.objects.latest("date_created").date_created
			url = 'https://bkkapp.nhso.go.th/bkkapp/api/v1/public/HelpdeskReportService/get_total_hosp'
			query = "select sum(req_claimcode::int) from crm_model5_recap_report"
			querySumReqClaim = "select sum(req_claim::int) from crm_model5_recap_report"
			querySumApprove = "select sum(approved::int) from crm_model5_recap_report"
			querySumDenined = "select sum(denined::int) from crm_model5_recap_report"
			queryCountHospSendClaim = "select count(*) from crm_model5_recap_report where approved not in ('0')"
			queryCountHospNoSendClaim = "select count(*) from crm_model5_recap_report where approved in ('0')"
			querySumDataKnow = "select sum(dataknow ::int) from crm_model5_recap_report"
			querySumOver = FnQueryOne("select sum(over5day::int) from crm_dataTimePeriod") 
			# print(querySumOver[0])
			cursor.execute(query)
			results = cursor.fetchone()
			cursor.execute(querySumReqClaim)
			resultsReqClaim = cursor.fetchone()
			cursor.execute(querySumApprove)
			resultsApprov = cursor.fetchone()
			cursor.execute(querySumDenined)
			resultsDenined = cursor.fetchone()
			cursor.execute(queryCountHospSendClaim)
			countHospSendClaim = cursor.fetchone()
			cursor.execute(queryCountHospNoSendClaim)
			countHospNoSendClaim = cursor.fetchone()
			cursor.execute(querySumDataKnow)
			_SumDataKnow = cursor.fetchone()
			sum_ReqClaimCode  = "{:,}".format(results[0])
			sum_resultsReqClaim = "{:,}".format(resultsReqClaim[0])
			sum_Approv  = "{:,}".format(resultsApprov[0])
			sum_Denined = "{:,}".format(resultsDenined[0])
			SumDataKnow = "{:,}".format(_SumDataKnow[0])
			_querySumOver ="{:,}".format(querySumOver[0]) 
			respones = requests.get(url)
			sum_hosp = respones.json()
			persentSendClaimcode = "{:.{}f}".format( (int(countHospSendClaim[0])/count_hosp)*100, 0 ) 
			persentNoSendClaimcode = "{:.{}f}".format( (int(countHospNoSendClaim[0])/count_hosp)*100, 0 ) 
			context = {'sum_hosp': sum_hosp,'sum_ReqClaimCode':sum_ReqClaimCode,"sum_resultsReqClaim":sum_resultsReqClaim,
			"sum_Approv":sum_Approv,"sum_Denined":sum_Denined,"max_date":max_date,"count_installApp":count_installApp,
			"count_training":count_training,"countHospReqClaim":countHospReqClaim,
			"countHospSendClaim":countHospSendClaim[0],
			"persentSendClaimcode":persentSendClaimcode,
			"persentNoSendClaimcode":persentNoSendClaimcode,
			"SumDataKnow":SumDataKnow,"querySumOver":_querySumOver
			}
			return render(request, 'dashboard.html', context)
	except:
		with connection.cursor() as cursor:
			recap_report = model5_recap_report.objects.all()
			count_hosp = model5_recap_report.objects.all().count()
			count_installApp = Hospitals.objects.filter(install_app='Yes').count()
			count_training = Hospitals.objects.filter(training='Yes').count()
			countHospReqClaim = model5_recap_report.objects.filter(~Q(req_claimcode='0')).count()
			max_date = model5_recap_report.objects.latest("date_created").date_created
			url = 'https://bkkapp.nhso.go.th/bkkapp/api/v1/public/HelpdeskReportService/get_total_hosp'
			query = "select sum(req_claimcode::int) from crm_model5_recap_report"
			querySumReqClaim = "select sum(req_claim::int) from crm_model5_recap_report"
			querySumApprove = "select sum(approved::int) from crm_model5_recap_report"
			querySumDenined = "select sum(denined::int) from crm_model5_recap_report"
			queryCountHospSendClaim = "select count(*) from crm_model5_recap_report where approved not in ('0')"
			queryCountHospNoSendClaim = "select count(*) from crm_model5_recap_report where approved in ('0')"
			cursor.execute(query)
			results = cursor.fetchone()
			cursor.execute(querySumReqClaim)
			resultsReqClaim = cursor.fetchone()
			cursor.execute(querySumApprove)
			resultsApprov = cursor.fetchone()
			cursor.execute(querySumDenined)
			resultsDenined = cursor.fetchone()
			cursor.execute(queryCountHospSendClaim)
			countHospSendClaim = cursor.fetchone()
			cursor.execute(queryCountHospNoSendClaim)
			countHospNoSendClaim = cursor.fetchone()
			sum_ReqClaimCode  = "{:,}".format(results[0])
			sum_resultsReqClaim = "{:,}".format(resultsReqClaim[0])
			sum_Approv  = "{:,}".format(resultsApprov[0])
			sum_Denined = "{:,}".format(resultsDenined[0])
			respones = requests.get(url)
			sum_hosp = respones.json()
			persentSendClaimcode = "{:.{}f}".format( (int(countHospSendClaim[0])/count_hosp)*100, 0 ) 
			persentNoSendClaimcode = "{:.{}f}".format( (int(countHospNoSendClaim[0])/count_hosp)*100, 0 ) 
			context = {'sum_hosp': sum_hosp,'sum_ReqClaimCode':sum_ReqClaimCode,"sum_resultsReqClaim":sum_resultsReqClaim,
			"sum_Approv":sum_Approv,"sum_Denined":sum_Denined,"max_date":max_date,"count_installApp":count_installApp,
			"count_training":count_training,"countHospReqClaim":countHospReqClaim,
			"countHospSendClaim":countHospSendClaim[0],
			"persentSendClaimcode":persentSendClaimcode,
			"persentNoSendClaimcode":persentNoSendClaimcode
			}
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

def FnRecapReport(hcode,hname,req_claimcode,req_claim,approved,denined,dataknow,date_created):
	with connection.cursor() as cursor:
		query = "INSERT INTO crm_model5_recap_report(hcode, hname, req_claimcode, req_claim, approved, denined, dataknow , date_created) VALUES ('{}', '{}', '{}', '{}', '{}', '{}' ,'{}','{}')".format(hcode,hname,req_claimcode,req_claim,approved,denined,dataknow,date_created)
		cursor.execute(query)

def FnInsertTimePeriod(hcode,hname,over,under):
	with connection.cursor() as cursor:
		query = "INSERT INTO public.crm_datatimeperiod(hcode, hname, over5day, under5day) VALUES ('{}', '{}', '{}', '{}')".format(hcode,hname,over,under)
		cursor.execute(query)

def CreateTimePeriod():
		TimePeriod = datatimeperiod.objects.all()
		TimePeriod.delete()
		urlTimePeriod = 'https://bkkapp.nhso.go.th/bkkapp/api/v1/public/DataService/query/Time_period'
		respones = requests.get(urlTimePeriod)
		jsonTimePeriod = respones.json()
		for i in range(len(jsonTimePeriod['data'])):
			hcode = jsonTimePeriod['data'][i]['HCODE']
			hname = jsonTimePeriod['data'][i]['HNAME']
			over =  jsonTimePeriod['data'][i]['OVER_5DAY']
			under = jsonTimePeriod['data'][i]['UNDER_5DAY']
			FnInsertTimePeriod(hcode,hname,over,under)


def FnQueryOne(query):
	with connection.cursor() as cursor:
		cursor.execute(query)
		results = cursor.fetchone()
		return results



def recepreport(request):
	with connection.cursor() as cursor:
			query_sumErr = """
					select cr.hcode,ch.install_app,ch.training ,cr.hname ,cr.req_claimcode ,cr.req_claim ,cr.approved,cr.denined 
					from crm_hospitals ch 
					right join crm_model5_recap_report cr on ch.code = cr.hcode 
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
	context = {'recap_report': resultsList}
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
	with connection.cursor() as cursor:
				query_sumErr = """
	 					select s.hcode ,s.hname from crm_model5_recap_report s where approved not in ('0')
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
				context = {"amountHospReqClaim":resultsList}
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
	with connection.cursor() as cursor:
		query_sumErr = """
			select hcode ,hname,approved 
			from crm_model5_recap_report
			where approved not in ('0')
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




def ListHospNotClaim(request):
	with connection.cursor() as cursor:
				query_sumErr = """
	 					select s.hcode ,s.hname from crm_model5_recap_report s where approved in ('0')
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
	context = {'listHospNotReqClaim': resultsList}
	return render(request,'amountHospNotReqClaim.html',context)





class ChartHospSendClaimCode(APIView):
	def get(self, request, format=None):
		with connection.cursor() as cursor:
				query_sumErr = """
	 					select count(*) from crm_model5_recap_report where approved not in ('0')
	 				"""
				query = """
	 					select count(*) from crm_model5_recap_report where approved in ('0')
	 				"""
				cursor.execute(query_sumErr)
				results = cursor.fetchone()
				cursor.execute(query)
				results_ = cursor.fetchone()

				countHospSendNoClaim = results[0]
				countHospSendClaim = results_[0]
		labels = ['ส่งเบิก', 'ไม่ส่งเบิก']
		default_items = [countHospSendNoClaim,countHospSendClaim]
		data = {"labels": labels,
            "default": default_items,
        }
		return Response(data)



class ChartAmountHospSendClaim(APIView):
		def get(self, request, format=None):
			with connection.cursor() as cursor:
				query = """
	 					select sum(req_claim::int) as claim ,sum(approved::int) as approved ,sum(denined::int) as denined
						from crm_model5_recap_report cmrr 
	 				"""
				cursor.execute(query)
				results = cursor.fetchall()
				print(results)
				countHospSendNoClaim = 0
				countHospSendClaim = 0
				labels = ['ผ่านการตรวจสอบ', 'ไม่ผ่านการตรวจสอบ']
				default_items = [countHospSendNoClaim,countHospSendClaim]
				data = {"labels": labels,
					"default": default_items,
				}
			return Response(data)


def dataKnowReqClaimCode(request):
	with connection.cursor() as cursor:
				query = """
	 					select hcode,hname,dataknow 
						from crm_model5_recap_report
						order by hcode::int
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
				context = {"DataKnowReqClaimCode":resultsList}
	return render(request, 'DataKnowReqClaimCode.html', context)


def dataTimePeriodOver(request):
	timeperiod = datatimeperiod.objects.all()
	context = {"timeperiod":timeperiod}
	return render(request, 'dataTimePeriodOver.html', context)
