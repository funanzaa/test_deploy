from django.db import connection
from .models import *

def checkRequest(id=None):
    with connection.cursor() as cursor:
        query = """
                    select count(*)
                    from "profileErefer_profileereferral" pep 
                    inner join crm_profileserver ps on pep."ProfileServer_id" = ps.id 
                    where ps.hospitals_id = %(_id)s
            """
        cursor.execute(query, {'_id': id})
        result = cursor.fetchone()
        return result[0]

def ListSetupErefer():
    with connection.cursor() as cursor:
        query = """
        select pep.*,hos.*
        from "profileErefer_profileereferral" pep 
        inner join crm_profileserver ps on pep."ProfileServer_id" = ps.id 
        inner join (
            select hos.*,m_hos.code as refer_code,m_hos.label as refer_label
            from crm_hospitals hos 
            left join crm_main_hospital m_hos on hos.main_hospital::int = m_hos.id
        ) as hos on hos.id = ps.hospitals_id 
        where pep."ServerServiceStatus_id" = 1
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

def view_server_profile(id=None):
    with connection.cursor() as cursor:
        query = """
        select pep.*,hos.*,ps.*
        from "profileErefer_profileereferral" pep 
        inner join crm_profileserver ps on pep."ProfileServer_id" = ps.id 
        inner join (
            select hos.*,m_hos.code as refer_code,m_hos.label as refer_label
            from crm_hospitals hos 
            left join crm_main_hospital m_hos on hos.main_hospital::int = m_hos.id
        ) as hos on hos.id = ps.hospitals_id 
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