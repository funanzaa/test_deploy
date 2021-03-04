from django.db import connection
from django.shortcuts import render, redirect
from .models import *
import datetime
import pytz

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

def deshboardSetupEreferral(hcode):
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
        where q.refer_code = '%(_hcode)s'
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