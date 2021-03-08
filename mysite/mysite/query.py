from django.db import connection
import datetime
import pytz



def checkInsert(day):
    with connection.cursor() as cursor:
        query = """
        select date_part('day',max(date_created )) 
        from crm_model5_recap_report cmrr
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return True if int(day) == result[0] else False
