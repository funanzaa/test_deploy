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

def insertProfileErefer(FirstName,LastName,ContactPhone,ServerServiceStatus,request_date,memo):
    with connection.cursor() as cursor:
        query="""
        INSERT INTO public."profileErefer_profileereferral" ("ContactFirstName","ContactLastName","ContactPhone"
        , "ServerServiceStatus_id",request_at,"EreferMemo") VALUES('{}','{}','{}',{},'{}','{}');
        """.format(FirstName,LastName,ContactPhone,ServerServiceStatus,request_date,memo)
        cursor.execute(query)

def findProfileId(id):
    with connection.cursor() as cursor:
        query = """
        select cp.id from crm_profileserver cp where cp.hospitals_id = %(_id)s
        """
        cursor.execute(query, {'_id': id})
        result = cursor.fetchone()
        return result[0]

def ListOverAllHc():
    with connection.cursor() as cursor:
        query = """
      select pep.*,hos.*
      ,ps.id as ProfileServer_id, ps."ContactPhone", ps."FixIpAddress", ps."datetimeSendServer", ps."Memo", ps."ContactFirstName", ps."ContactLastName", ps."ContactEmail", ps."datetimeReceiveServer", ps."ServerImage", ps."UseServer", ps."dbBackup", ps."datetimeCompleteServer", ps.update_at, ps."OperationSystem_id", ps."ServerBand_id", ps."ServerServiceStatus_id", ps.created_by_id, ps.database_id, ps.hospitals_id, ps."webServer_id", ps.update_by 
      ,auth_user.first_name as staff_first_name ,auth_user.last_name as staff_last_name
       ,auth_user_update.first_name as staff_update_first_name ,auth_user_update.last_name as staff_update_last_name,crm_serverband."name" as band_server
       ,crm_operationsystem."name" as os_name,crm_serverservicestatus."name" as server_status
        from "profileErefer_profileereferral" pep 
        inner join crm_profileserver ps on pep."ProfileServer_id" = ps.id 
        inner join (
            select hos.*,m_hos.code as refer_code,m_hos.label as refer_label
            from (select * from crm_hospitals hos where hos.main_hospital = '6') hos 
            left join crm_main_hospital m_hos on hos.main_hospital::int = m_hos.id
        ) as hos on hos.id = ps.hospitals_id 
        left join auth_user on pep.created_by::int = auth_user.id 
        left join auth_user as auth_user_update on pep.update_by ::int = auth_user_update.id 
        left join crm_serverband on ps."ServerBand_id" = crm_serverband.id 
        left join crm_operationsystem on ps."OperationSystem_id" = crm_operationsystem.id 
        left join crm_serverservicestatus on pep."ServerServiceStatus_id" = crm_serverservicestatus.id 
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

def ListAllReferral():
    with connection.cursor() as cursor:
        query = """
            select erefer.main_hcode,main_label,erefer.hos_code,erefer.hos_label
            ,st."name"  
            ,pep."ContactFirstName" || ' ' || pep."ContactLastName" as contact
            ,pep."ContactPhone" as contact_phone
            ,case when pep."success_at" is null then pep.case_lock_date_time else pep."success_at" end as success_at
            ,case when st."name" = 'ติดตั้งเรียบร้อย' then pep."EreferMemo" 
                when st."name" = 'ติดตั้งไม่สำเร็จ' then pep."EreferMemo" 
                else pep."EreferMemo" end as Memo
            ,case when st."name" = 'รับเข้าระบบ' then user_lock.first_name || ' ' || user_lock.last_name 
                else auth_user.first_name || ' ' || auth_user.last_name end as staff
            ,pep."ProfileServer_id" as ProfileServer_id
            ,case when st."name" = 'รับเข้าระบบ' then user_lock.id
                else auth_user.id end as staff_id
            ,pep."testData" as testData
            ,pep."testMq" as testMq
            from (
                select cmh.code as main_hcode,cmh."label" as main_label ,ch.code as hos_code,ch."label" hos_label ,ch.id
                from crm_hospitals ch  
                inner join crm_main_hospital cmh on ch.main_hospital::int = cmh.id 
                where ch.main_hospital <> '0' and ch.main_hospital <> '6'
                order by main_hcode
            ) as erefer
            inner join crm_profileserver cp on erefer.id = cp.hospitals_id 
            inner join "profileErefer_profileereferral" pep on cp.id = pep."ProfileServer_id" 
            left join auth_user on pep.created_by::int = auth_user.id 
            left join auth_user user_lock on pep.case_staff_lock::int = user_lock.id 
            left join crm_serverservicestatus st on pep."ServerServiceStatus_id" = st.id 
            order by erefer.main_hcode
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

def export_csv():
    with connection.cursor() as cursor:
        query = """
    select erefer.main_hcode,main_label,erefer.hos_code,erefer.hos_label
    ,st."name" 
    ,case when st."name" = 'ติดตั้งเรียบร้อย' then '' 
        when st."name" = 'ติดตั้งไม่สำเร็จ' then pep."EreferMemo" 
        else pep."EreferMemo" end as Memo
    ,case when st."name" = 'รับเข้าระบบ' then user_lock.first_name || ' ' || user_lock.last_name 
        else auth_user.first_name || ' ' || auth_user.last_name end as staff
    from (
        select cmh.code as main_hcode,cmh."label" as main_label ,ch.code as hos_code,ch."label" hos_label ,ch.id
        from crm_hospitals ch  
        inner join crm_main_hospital cmh on ch.main_hospital::int = cmh.id 
        where ch.main_hospital <> '0' and ch.main_hospital <> '6'
        order by main_hcode
    ) as erefer
    inner join crm_profileserver cp on erefer.id = cp.hospitals_id 
    inner join "profileErefer_profileereferral" pep on cp.id = pep."ProfileServer_id" 
    left join auth_user on pep.created_by::int = auth_user.id 
    left join auth_user user_lock on pep.case_staff_lock::int = user_lock.id 
    left join crm_serverservicestatus st on pep."ServerServiceStatus_id" = st.id 
    order by erefer.main_hcode
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