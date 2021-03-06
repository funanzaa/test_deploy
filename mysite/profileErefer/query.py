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
        and pep.case_locking = '0'
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

def countRequestErefer():
    with connection.cursor() as cursor:
        query = """
        select count(*)
        from "profileErefer_profileereferral" ss
        where ss."ServerServiceStatus_id" = 1
        and ss.case_locking = '0'
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]

def ListVersErefws():
    with connection.cursor() as cursor:
        query = """
        select * from "profileErefer_verserefws"
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


def ListServerservicestatus():
    with connection.cursor() as cursor:
        query = """
        select * from crm_serverservicestatus cs where cs.id in (2,4)
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

def ListStatusCaseErefer(id,user):
    with connection.cursor() as cursor:
        query = """
        select count(*)
        from "profileErefer_profileereferral" ss
        where ss."ServerServiceStatus_id" = %(_id)s
        and ss.case_staff_lock = '%(_user)s'
        """
        cursor.execute(query, {'_id': id,'_user': user })
        result = cursor.fetchone()
        return result[0]


def ListSetupEreferStatus(id,user):
    with connection.cursor() as cursor:
        query = """
        select pep.*,hos.*,auth_user.first_name as staff_first_name ,auth_user.last_name as staff_last_name
        ,auth_user_update.first_name as staff_update_first_name ,auth_user_update.last_name as staff_update_last_name
        from "profileErefer_profileereferral" pep 
        inner join crm_profileserver ps on pep."ProfileServer_id" = ps.id 
        inner join (
            select hos.*,m_hos.code as refer_code,m_hos.label as refer_label
            from crm_hospitals hos 
            left join crm_main_hospital m_hos on hos.main_hospital::int = m_hos.id
        ) as hos on hos.id = ps.hospitals_id 
        left join auth_user on pep.created_by::int = auth_user.id 
        left join auth_user as auth_user_update on pep.update_by ::int = auth_user_update.id 
        where pep."ServerServiceStatus_id" = %(_id)s
        and pep."case_staff_lock" = '%(_user)s'
        """
        cursor.execute(query, {'_id': id,'_user':user})
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

def insert_profileErefer(update_at,success_at,status_case,user,versErefws,versHosErefer,ereferMemo,testData,testMq,pk):
    with connection.cursor() as cursor:
        query="""
        UPDATE "profileErefer_profileereferral" SET  update_at='{}', success_at='{}'
        ,"ServerServiceStatus_id"={}
        , created_by='{}', "versErefws_id"={}
        , "versHosEreferral_id"={},  "EreferMemo"='{}'
        , "testData"='{}', "testMq"='{}'
        WHERE "ProfileServer_id" = {};
        """.format(update_at,success_at,status_case,user,versErefws,versHosErefer,ereferMemo,testData,testMq,pk)
        cursor.execute(query)

def update_profileErefer(update_at,status_case,user,versErefws,versHosErefer,ereferMemo,testData,testMq,pk):
    with connection.cursor() as cursor:
        query="""
        UPDATE "profileErefer_profileereferral" SET  update_at='{}'
        ,"ServerServiceStatus_id"={}
        , created_by='{}', "versErefws_id"={}
        , "versHosEreferral_id"={},  "EreferMemo"='{}'
        , "testData"='{}', "testMq"='{}'
        WHERE "ProfileServer_id" = {};
        """.format(update_at,status_case,user,versErefws,versHosErefer,ereferMemo,testData,testMq,pk)
        cursor.execute(query)
