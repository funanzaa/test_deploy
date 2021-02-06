from django.db import connection
from django.shortcuts import render, redirect


def queryProject(pk):
        with connection.cursor() as cursor:
            query = """
            select  CONCAT(cc."app_controlVersion", ' | ', cc."hos_s_version") AS "app_controlVersion",
            CONCAT(cc."hos_stock_version", ' | ', cc."hos_ereferral_version") AS "app_hosVersion"
            ,ch.label 
            ,cc.date_created 
            ,cc.hcode 
            FROM crm_controlversion cc
            left join crm_hospitals ch on cc.hcode = ch.code
            where cc.hcode not in ('sql fail')
            order by date_created desc;
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
            context = {'ControlVersion': resultsList}
        return context


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