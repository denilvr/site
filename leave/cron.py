from datetime import datetime
from leave.models import Employee
from leave.models import EmployeeLeaveMaster
from leave.models import EmployeeLeaveLog
from django.core.mail import send_mail,EmailMessage
from datetime import datetime, date, timedelta
import unicodedata
from dateutil import parser
##from leave.models import *
import calendar
from decimal import *

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

def leaves(date):
    date = parser.parse(date)
    j_year=date.year
    j_month=date.month
    today = datetime. now()
    c_year=today.year
    c_month=today.month
    if c_month<4:
        f_year=[datetime(c_year-1,3,31),datetime(c_year,3,31)]
        temp = (j_year > f_year[0].year and j_year <= f_year[1].year)
    if c_month>=4:
        f_year = [datetime(c_year,3,31), datetime(c_year+1,3,31)]
        temp=(j_year >= f_year[0].year and j_year < f_year[1].year)
    if (date>f_year[0] and date<f_year[1]):

        if j_month<4:
            curr_financial=datetime(j_year,3,31)
            days_left=curr_financial-date
            days_left=(days_left.days)+1
        elif j_month>=4:
            curr_financial=datetime(j_year+1,3,31)
            days_left=curr_financial-date
            days_left=(days_left.days)+1
    else:
        days_left=365
    num=float(days_left*12)
    num1=float(days_left*10)
    getcontext().prec = 3
    cl = float(Decimal(num) /Decimal(365))
    sl = float(Decimal(num) /Decimal(365))
    el = float(Decimal(num1) /Decimal(365))

    leaves = {
        'cl': cl,
        'sl': sl,
        'el': el,
        }
    return leaves


def annual(date):
    date= parser.parse(date)
    today=datetime.now()
    t_month=today.month
    t_year=today.year
    j_month=date.month
    j_year=date.year
    if (j_month == t_month and j_year==t_year):
        temp=datetime(j_year,j_month,calendar.monthrange(j_year,j_month)[1])
        days_left=temp-date
        days_left=(days_left.days)+1
        al=((days_left)/calendar.monthrange(j_year,j_month)[1])*1.25
    else:
        c_date = datetime(t_year, t_month, calendar.monthrange(t_year, t_month)[1]).date()
        d=c_date-date.date()
        days=d.days
        days_left=float(days+1)
        months=days_left/calendar.monthrange(t_year, t_month)[1]
        months=round(months)
        print(months)
        num1 = float(days_left * 15)
        getcontext().prec = 3
        al = float(Decimal(num1) / Decimal(365))
    if al>45:
    	al-=45
    else:
    	pass
    return al

'''
def leaves_increment():
	e=Employee.objects.all()
	for i in e:
		lm=EmployeeLeaveMaster.objects.get(empID=i.empID)
		leave_left=leaves(i.joiningDate)
		cl=leave_left.get('cl',None)
		sl=leave_left.get('sl',None)
		el=leave_left.get('el',None)
		if i.gender=='Female':
			ml=60
		else:
			ml=0
		lm.casualLeavesLeft=cl
		lm.sickLeavesLeft=sl
		lm.earnleavesLeft=fl
		lm.maternityLeavesLeft=ml
		lm.save()
def annual_leaves_increment():
	e=Employee.objects.all()
	for i in e:
		lm=EmployeeLeaveMaster.objects.get(empID=i.empID)
		leave_left=annual(i.joiningDate)
		lm.vacationLeavesLeft=leave_left
		lm.maternityLeavesLeft=ml
		lm.save()

'''