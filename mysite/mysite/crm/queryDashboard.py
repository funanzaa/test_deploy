from django.db import connection
from django.shortcuts import render, redirect


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