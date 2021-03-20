from django.db import connection
from django.shortcuts import render, redirect
from .models import *
import datetime
import pytz
import json
import requests

def queryProjectAll(project,month):
    with connection.cursor() as cursor:
        query = """
            select count(*)
            from crm_case cc
            inner join (
                        select cps.id 
                        from crm_project_subgroup cps 
                        inner join crm_project cp on cps.project_id = cp.id 
                        where cp."name" = %(_project)s
                        ) project_subgroup on project_subgroup.id = cc.project_subgroup_id
            where date_part('month',cc.date_entered) = %(_month)s
        """
        cursor.execute(query, {'_project': project,'_month': month})
        result = cursor.fetchone()
        return result[0]

def fnReportOpbkkWeb(project,month):
    with connection.cursor() as cursor:
        query = """
                    select count(*)
                    from crm_case cc 
                    where cc.project_subgroup_id = %(_project)s
                    and date_part('month',cc.date_entered) = %(_month)s
            """
        cursor.execute(query, {'_project': project,'_month': month})
        result = cursor.fetchone()
        return result[0]

def countRequestErefer():
    with connection.cursor() as cursor:
        query = """
        select count(*)
        from "profileErefer_profileereferral" ss
        where ss."ServerServiceStatus_id" = 1
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]

def checkRequestServerDup(hospital):
    with connection.cursor() as cursor:
        query = """
        select count(*) from crm_profileserver cp where hospitals_id = %(_hospital)s and "ServerServiceStatus_id" = 1
        """
        cursor.execute(query, {'_hospital': hospital})
        result = cursor.fetchone()
        return result[0]

def deshboardSetupEreferral(hcode=None):
    with connection.cursor() as cursor:
        query = """
        select q.refer_code,q.refer_label,q.status_success,q.status_total,((q.status_success * 100)/q.status_total)::numeric(5,2) as percentage
        from (
                select hos.refer_code,hos.refer_label
                ,sum(case when pep."ServerServiceStatus_id" in ('2') then 1 else 0 end) as status_success
                ,sum(case when pep."ServerServiceStatus_id" in ('4','1','2') then 1 else 0 end) as status_total
                from "profileErefer_profileereferral" pep 
                inner join crm_profileserver ps on pep."ProfileServer_id" = ps.id 
                inner join (
                    select hos.*,m_hos.code as refer_code,m_hos.label as refer_label
                    from crm_hospitals hos 
                    left join crm_main_hospital m_hos on hos.main_hospital::int = m_hos.id
                ) as hos on hos.id = ps.hospitals_id 
                group by hos.refer_code,hos.refer_label
            ) q
        --where q.refer_code = '%(_hcode)s'
        """
        cursor.execute(query, {'_hcode': hcode})
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

def queryProfileEreferral(id):
    with connection.cursor() as cursor:
        query = """
        select pep.*,hos.*,auth_user.first_name as staff_first_name ,auth_user.last_name as staff_last_name
        ,auth_user_update.first_name as staff_update_first_name ,auth_user_update.last_name as staff_update_last_name
        ,ws."name" as ws_name ,hs."name" as hs_name,serverStatus."name" as serverStatus_name
        from "profileErefer_profileereferral" pep 
        inner join crm_profileserver ps on pep."ProfileServer_id" = ps.id 
        inner join (
            select hos.*,m_hos.code as refer_code,m_hos.label as refer_label
            from crm_hospitals hos 
            left join crm_main_hospital m_hos on hos.main_hospital::int = m_hos.id
        ) as hos on hos.id = ps.hospitals_id 
        left join auth_user on pep.created_by::int = auth_user.id 
        left join auth_user as auth_user_update on pep.update_by ::int = auth_user_update.id 
        left join "profileErefer_verserefws" ws on  pep."versErefws_id" = ws.id 
        left join "profileErefer_vershosereferral" hs on pep."versHosEreferral_id" = hs.id 
        left join crm_serverservicestatus serverStatus on pep."ServerServiceStatus_id" = serverStatus.id 
        where pep."ProfileServer_id" = %(_id)s
        """
        cursor.execute(query, {'_id': id})
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

def ListProfileServerAll():
       with connection.cursor() as cursor:
        query = """
        select ps.*,pep."ServerServiceStatus_id" as erefer_status,hos.code,hos."label",band."name" as ServerBand
        from crm_profileserver ps
        left join "profileErefer_profileereferral" pep on ps.id = pep."ProfileServer_id"  
        left join crm_hospitals hos  on ps.hospitals_id = hos.id 
        left join crm_serverband band on ps."ServerBand_id" = band.id 
        order by ps.id desc
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
        select to_char(date_part('day',(current_timestamp - min(api.insert_at))),'FM999999990') as timeday
        ,to_char(date_part('hour',(current_timestamp - min(api.insert_at))),'FM999999990') as timehour
        ,to_char(date_part('minute',(current_timestamp - min(api.insert_at))),'FM999999990')  as timeminute
        ,to_char(date_part('second',(current_timestamp - min(api.insert_at))),'FM999999990')  as timesecond
        from "apiCases_apiappnhsobkk" api 
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


def detailCaseApi(id):
    with connection.cursor() as cursor:
        query= """
        select cc.*
        ,api.id as api_id, api.callback_id, api.callback_code, api.callback_title, api.callback_group_id
        , api.callback_subgroup_id, api.callback_tag, api.staff_id, api.profile
        , api.callback_name, api.mobile_phone, api.detail, api.insert_at, api.case_locking
        , api.case_lock_date_time, api.case_staff_lock,cps.*,hos.code as hos_code ,hos."label" as hos_name
        from crm_case cc 
        inner join "apiCases_apiappnhsobkk" api on api.id = cc."apiCases_id"::int
        inner join (
                    select crm_project_subgroup.id as sub_id ,crm_project_subgroup.name as sub_name ,crm_project.name  as pro_name
                    from crm_project_subgroup 
                    inner join crm_project on crm_project.id = crm_project_subgroup.project_id 
        ) cps on cps.sub_id = cc.project_subgroup_id 
        inner join crm_hospitals hos on hos.id = cc.hospitals_id 
        where cc.created_by_id = %(_id)s
        """
        cursor.execute(query, {'_id': id})
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

def countCaseApi(id):
    with connection.cursor() as cursor:
        query= """
        select count(cc.id)
        from crm_case cc 
        inner join "apiCases_apiappnhsobkk" api on api.id = cc."apiCases_id"::int
        inner join (
                    select crm_project_subgroup.id as sub_id ,crm_project_subgroup.name as sub_name ,crm_project.name  as pro_name
                    from crm_project_subgroup 
                    inner join crm_project on crm_project.id = crm_project_subgroup.project_id 
        ) cps on cps.sub_id = cc.project_subgroup_id 
        inner join crm_hospitals hos on hos.id = cc.hospitals_id 
        where cc.created_by_id = %(_id)s
        and cc."status_Case_id" is null
        """
        cursor.execute(query, {'_id': id})
        result = cursor.fetchone()
        return result[0]

def postStatus3(CALLBACK_CODE,callback_reply,staff,date):
    data = { "callback_status" : 3,
            "callback_reply" : callback_reply,
            "callback_by" : staff,
            "callback_date": date
            }
    json_object = json.dumps(data) 
    url = 'https://bkkapp.nhso.go.th/bkkapp/api/v1/public/HelpdeskReportService/update_callback_result/{}'.format(CALLBACK_CODE)
    r = requests.post(url, data=json_object)
    print(r.text)

def getNameLastName(id):
    with connection.cursor() as cursor:
        query= """
            select au.first_name || ' ' || au.last_name  as staff_name
            from auth_user au 
            where id = %(_id)s
            """
        cursor.execute(query, {'_id': id})
        result = cursor.fetchone()
        return result[0]