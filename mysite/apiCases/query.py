from django import urls
from django.db import connection
from django.db.models import query
from django.shortcuts import render, redirect
from .models import *
import datetime
import pytz
import requests
import json


def ListinsertApi():
    with connection.cursor() as cursor:
        query="""
        select cps.* as sub_name,api.*,hos.code , hos."label",hos.id as hos_id
        from (
                select crm_project_subgroup.id as sub_id ,crm_project_subgroup.name as sub_name ,crm_project.name  as pro_name
                from crm_project_subgroup 
                inner join crm_project on crm_project.id = crm_project_subgroup.project_id 
                ) cps 
        right join "apiCases_apiappnhsobkk" api on cps.sub_id = api.callback_subgroup_id::int
        left join crm_hospitals hos on hos.code = api.profile
        where api.case_locking = '0'
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
        return resultsList

def postStatus2(CALLBACK_CODE):
    data = { "callback_status" : 2}
    json_object = json.dumps(data) 
    url = 'https://bkkapp.nhso.go.th/bkkapp/api/v1/public/HelpdeskReportService/update_callback_result/{}'.format(CALLBACK_CODE)
    r = requests.post(url, data=json_object)

def countNotificationsAPI():
    with connection.cursor() as cursor:
        query = """
        select count(*) from "apiCases_apiappnhsobkk" api where api.case_locking = '0'       
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]

def TimeApiInsert():
    with connection.cursor() as cursor:
        query = """
        select to_char(date_part('hour',(current_timestamp - min(api.insert_at))),'FM999999990') as timehour
        ,to_char(date_part('minute',(current_timestamp - min(api.insert_at))),'FM999999990')  as timeminute
        ,to_char(date_part('second',(current_timestamp - min(api.insert_at))),'FM999999990')  as timesecond
        from "apiCases_apiappnhsobkk" api where api.case_locking = '0'
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
        return resultsList