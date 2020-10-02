import datetime
import pytz
from django import template
from ..models import Case
register = template.Library()


@register.filter
def round_number(number):
    tz = pytz.timezone('Asia/Bangkok')
    now = (datetime.datetime.now(tz=tz))
    count_case_total = Case.objects.filter(date_entered__month=now.month).count()
    return round((number*100)/count_case_total)
