import datetime
from datetime import timedelta
import pytz
from django import template
from ..models import Case
from django.contrib.auth.models import User
register = template.Library()


@register.filter
def getAssignName(pk=0):
    if pk == 0 :
        return ''
    elif pk == None :
        return ''
    else:
        name = User.objects.get(id=int(pk))
        return name.first_name + ' ' + name.last_name


@register.filter
def round_number(number=0):
    if number == 0 :
        return 0
    elif number == None :
        return 0
    else:
        tz = pytz.timezone('Asia/Bangkok')
        now = (datetime.datetime.now(tz=tz))
        count_case_total = Case.objects.filter(date_entered__month=now.month).count()
        return round((number*100)/count_case_total)

@register.filter
def add_datetime(time=None):
    if time == 0 :
        return "จาก Erefer"
    elif time == None :
        return "จาก Ereferal"
    else:
        hours_added = time + timedelta(hours=7)
        if hours_added.month == 1:
            month = ' มกราคม ' + str(hours_added.year + 543)
        elif hours_added.month == 2 :
            month = ' กุมภาพันธ์ ' + str(hours_added.year + 543)
        elif hours_added.month == 3:
            month = ' มีนาคม ' + str(hours_added.year + 543)
        elif hours_added.month == 4:
            month = ' เมษายน ' + str(hours_added.year + 543)
        elif hours_added.month == 5:
            month = ' พฤษภาคม ' + str(hours_added.year + 543)
        elif hours_added.month == 6:
            month = ' มิถุนายน ' + str(hours_added.year + 543)
        elif hours_added.month == 7:
            month = ' กรกฎาคม ' + str(hours_added.year + 543)
        elif hours_added.month == 8:
            month = ' สิงหาคม ' + str(hours_added.year + 543)
        elif hours_added.month == 9:
            month = ' กันยายน ' + str(hours_added.year + 543)
        elif hours_added.month == 10:
            month = ' ตุลาคม ' + str(hours_added.year + 543)
        elif hours_added.month == 11:
            month = ' พฤศจิกายน ' + str(hours_added.year + 543)
        elif hours_added.month== 12:
            month = ' ธันวาคม ' + str(hours_added.year + 543)

        return hours_added.strftime('%d') + month + hours_added.strftime(' %H:%M')

@register.filter
def formatNumber(number):
    fnumber = format(int(number), ',d')
    return fnumber


@register.filter
def calAssingCase(number):
    if number == 0 :
        return 0
    elif number == None :
        return 0
    else:
        now = (datetime.datetime.now(tz=tz))
        count_case_total = Case.objects.filter(date_entered__month=now.month).count()
        return round((number*100)/count_case_total)