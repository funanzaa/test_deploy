import datetime
from datetime import timedelta
import pytz
from django import template
# from ..models import Case
register = template.Library()


# @register.filter
# def round_number(number):
#     if number == 0 :
#         return 0
#     else:
#         tz = pytz.timezone('Asia/Bangkok')
#         now = (datetime.datetime.now(tz=tz))
#         count_case_total = Case.objects.filter(date_entered__month=now.month).count()
#         return round((number*100)/count_case_total)

@register.filter
def add_datetime(time):
    if time == 0 :
        return 0
    else:
        hours_added = time + timedelta(hours=7)
        return hours_added.strftime('%d %B %Y %H:%M')
