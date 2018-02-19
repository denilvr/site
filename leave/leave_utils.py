from datetime import datetime, date, timedelta
import unicodedata
from leave.models import *
import urllib
import ssl
import urllib.request
import sys
from urllib.request import urlopen, URLError
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import dateutil.parser
import re
import time
from decimal import *
from copy import deepcopy
import leave.get_values
date_format = "%Y-%m-%d"




def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def calculate_duration(startDate, endDate):
    getcontext().prec=3
    duration = (endDate - startDate).total_seconds()
    daygenerator = (startDate + timedelta(x + 1) for x in range((endDate - startDate).days))
    d=sum(1 for day in daygenerator if day.weekday() >= 5)
    duration_final=Decimal(duration)/3600
    
    duration_final=duration_final/Decimal(24)
    duration_final=duration_final-d
    holidays = is_holidays(startDate,endDate)
    duration_final=duration_final-holidays

    return duration_final


def string_to_date(date):
    # date_object=unicodedata.normalize('NFKD', date).encode('ascii','ignore')
    date_object = dateutil.parser.parse(date)
    return date_object


def validate_input(emp_id,leaveType,startDate, endDate):
    case=1
    case1=1
    #end_date_string=string_to_date(end_date)
    try:    
        start_date = dateutil.parser.parse(startDate)
        end_date = dateutil.parser.parse(endDate)
        date = datetime.datetime.today().date()
        d = calculate_duration(start_date, end_date)
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        last_date = datetime.datetime.today().date()+ datetime.timedelta(days=90)
        prior_date = start_week
        message=''
        case=1
        case1=1
        if (start_date.date() > last_date) or (start_date.date() < prior_date):
            case= 0

        else:
            if start_date <= end_date:

                if (leaveType == 'FLEXI LEAVE') and d <= 5:
                    case= 1
                elif (leaveType == 'FLEXI LEAVE') and d > 5:
                    case= 0
                elif (leaveType == 'CASUAL LEAVE') and d > 2:
                    case= 0
                else:
                    case= 1
            else:
                case= 0

        if case==0:
            message='This leave application cannot be proccessed. Please contact your manager.'
        yesterday = start_date.date()-timedelta(days=1)
        tomorrow = start_date.date()+timedelta(days=1)
        is_yesterday_holiday = is_holiday(yesterday)
        is_tomorrow_holiday = is_holiday(tomorrow)
        #print((is_yesterday_holiday and start_date.weekday()==2 and leaveType=='CASUAL LEAVE'),"******************")
        #print(is_yesterday_holiday)
        if ((is_yesterday_holiday and tomorrow.weekday(
            )==5 and leaveType=='CASUAL LEAVE') or (
        is_tomorrow_holiday and yesterday.weekday(
            )==6 and leaveType=='CASUAL LEAVE')) or (is_yesterday_holiday and start_date.weekday()==1 and leaveType=='CASUAL LEAVE') or ((tomorrow.weekday()>4 and is_holiday(start_date+timedelta(days=3))) and leaveType=='CASUAL LEAVE') or (start_date.weekday()==4 and is_holiday(start_date+timedelta(days=3)) and leaveType=='CASUAL LEAVE') or (get_values.can_cl_be_applied(emp_id,start_date,end_date,leaveType)==False ):
            temp1=get_values.can_cl_be_applied(emp_id,start_date,end_date,leaveType)
            
            if temp1==False and leaveType!='CASUAL LEAVE':
                message='leave cannot be proccessed. This leave application is clubbing with casual leave.'
            elif temp1==False and leaveType=='CASUAL LEAVE':
                message='leave cannot be proccessed. casual leave cannot be clubbed with other leaves.'
            else:
                message='You cannot apply casual leave on this day. If you want to apply leave on this day, please apply for annual leave.'
            case1=0
        else:
            case1=1
        p=is_holiday(start_date.date())
        q=is_holiday(end_date.date())
        if (p  and q) or (start_date.weekday()>4 and end_date.weekday()>4):
            message='Cannot apply leave on this day. It is a holiday.'
            case1=0
        if start_date>end_date:
            message = "Invalid start and end date."
    except:
        message='Something went wrong, please try again.'
    
    data={
    'case':case,
    'case1':case1,
    'message':message
    }
    return data


holiday_list=['2016-01-01', '2016-01-15', '2016-01-26', '2016-04-14', '2016-05-01', '2016-07-07', '2016-08-15', '2016-09-05', '2016-09-13', '2016-10-02', '2016-10-11', '2016-10-28', '2016-12-25', '2016-12-26', '2017-01-01', '2017-01-14', '2017-01-16', '2017-01-26', '2017-04-14', '2017-05-01', '2017-08-15', '2017-08-25', '2017-09-02', '2017-09-29', '2017-09-30', '2017-10-02', '2017-10-18', '2017-12-25']

def is_holiday(date):
    try:
        date = date.date()
    except:
        pass
    date = str(date)
    if date in holiday_list:
        return True
    else:
        return False


def is_holidays(start_date,end_date):
    d1 = start_date.date()
    d2 = end_date.date()

    

    delta = d2 - d1
    c=0

    for i in range(delta.days + 1):
        d= d1 + timedelta(days=i)

        if is_holiday(d)==1:
            c=c+1
        else:
            pass

    return c
    

def is_manager(empID,user_id):
    employee_instance = list(Employee.objects.filter(empID=user_id).values())  
    if (str(employee_instance[0]['managerID']) == str(empID)):
        return True
    else:
        return False

def is_HR(empID):
    print(empID)
    hr_instance = list(Employee.objects.filter(empID=empID).values())   
    print(hr_instance) 
    if hr_instance and hr_instance[0]['is_hr']==True:
        return True
    else:
        return False

def check_holidays(start,end):

    if (start.hour ==23 or start.hour==11) and (start.minute == 59
    ) and (start.second ==59):
        start=start+timedelta(seconds=1)
    if (end.hour ==00 or end.hour==12) and (end.minute == 00
    ) and (end.second ==00):
        end=end-timedelta(seconds=1)
    temp=deepcopy(start)
    
    days=[]

    if (start.isoweekday() in set((6, 7)) and ((start.date()!=end.date()) or start+timedelta(days=1)!=end)):
        start += datetime.timedelta(days=start.isoweekday() % 5)
        
    if end.isoweekday() in set((6, 7)) and (start.date()!=end.date()):
        end -= datetime.timedelta(days=end.isoweekday() % 5)
    while temp <= end:
        days.append(temp)
        if temp in holiday_list:
            days.remove(i)
        temp+=datetime.timedelta(days=1)
    data={
        'start date':start,
        'end date':end
    }
    return data    

































