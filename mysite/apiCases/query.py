from django.db import connection
from django.db.models import query
from django.shortcuts import render, redirect
from .models import *
import datetime
import pytz
import requests


def ListinsertApi():
    with connection.cursor() as cursor:
        query="""
        select p.name as pro_name,cps."name" as sub_name,hos.code as hos_code,hos."label" as hos_label
        ,aca.*
        from "apiCases_apiappnhsobkk" aca 
        left join crm_project_subgroup cps on aca.callback_subgroup_id::int = cps.id 
        left join crm_project p on cps.project_id = p.id
        left join crm_hospitals hos on aca.profile = hos.code 
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
    r = requests.post('https://bkkapp.nhso.go.th/bkkapp/api/v1/public/HelpdeskReportService/update_callback_result/{}'.format(CALLBACK_CODE))
    r_dict = r.json()
    print(r_dict['message_status'])