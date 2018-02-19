from __future__ import print_function
from django.shortcuts import render
from django.http import JsonResponse
from leave.models import (Employee,
	EmployeeProject,
	EmployeeLeaveLog,
	EmployeeLeaveMaster,
	EmployeeLeaveTransaction,
	PhoneNumber,
	EmployeeAddress,
	Logincredentials
	)
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.core import serializers
from sys import argv
import leave.leave_utils as leave_utils
import leave.get_values as get_values
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
import unicodedata

from datetime import timedelta,datetime
from django.core.mail import send_mail,EmailMessage
import xlrd
import csv
from csv import DictWriter
from dateutil import parser
import ast
from copy import deepcopy
from collections import OrderedDict
import pandas as pd

from urllib.parse import urlparse, parse_qs
from passlib.hash import pbkdf2_sha256
#from leave.forms import ContactForm
#from .forms import PostForm
import re
from .forms import CustomModelForm
from .forms import SignUpForm
from .forms import LeaveApplicationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required



date_format="%Y-%m-%d"


def string_to_date(date):
	date_object=unicodedata.normalize('NFKD', date).encode('ascii','ignore')
	date_object=parser.parse(date)
	return date_object
leavesLeft=['casualLeavesLeft','sickLeavesLeft','vacationLeavesLeft','earnLeavesLeft']
"""
This function deals with the leave application of te user. First the input checked whether it is valid or not according to the rules and if it is valid then
it calculates the duration and fetches employee id from Employee table. From Employee Leave Transaction table the details of that employee is fetched and checks
whether the eployee has taken leave or not.If the dates and leave are matching then returns a message that the employee has applied for leave already, if only dates are
matching and leave isn't then the leave is updated. leaves left is calculated later and if the leave is updating it'll update the number of leaves as well in database.
Sets False for the previous leave application.
"""
@csrf_exempt
def checkavailable(request):
	if request.method=='POST':
		check = json.loads(request.body)
		incoming= check.get('incoming',None)
		data={
		'status':'Success',
		}
		return JsonResponse(data)

# @csrf_exempt
# def create_user(request):
# 	if request.method=='POST':
# 		newuser_input = request.POST
# 		emplID = newuser_input.get('emplID',None)
# 		username = newuser_input.get('username',None)
# 		password = newuser_input.get('password',None)
# 		enc_password=pbkdf2_sha256.using(rounds=8000, salt_size=10).hash(password)
# 		Logincredentials.objects.create(username=username,password=enc_password, EmpID=emplID)
# 		data={
# 		'status':'Success', 'ID':str(emplID)
# 		}
# 		return JsonResponse(data)
# 	else:
# 		return render(request, 'lms/signup.html')

#All check
# @csrf_exempt
# def login_user(request):
# 	if request.method=='POST':
# 		existinguser_input = request.POST
# 		username = existinguser_input.get('username',None)
# 		password = existinguser_input.get('password',None)
# 		if Logincredentials.objects.filter(username=username).exists():
# 			pass_temp = Logincredentials.objects.filter(username=username).values('password')[0]['password']
# 			#pass_temp = re.findall(r"(?<= u')(.*?)(?='})",str(pass_temp))
# 			employeeeID= Logincredentials.objects.filter(username=username).values('EmpID')
# 			print(employeeeID)
# 			print(employeeeID[0])
# 			print(employeeeID[0]['EmpID'])
# 			ID=str(employeeeID[0]['EmpID'])
# 			print(ID)
# 			if pbkdf2_sha256.verify(password,pass_temp)==True:
# 				data={
# 				'message':'True' ,
# 				'ID': ID
# 				}
# 				return JsonResponse(data)
# 			else :
# 				data={'message':'False_1', 'ID':'NULL'}
# 				return JsonResponse(data)
			
# 		else:
# 			data={'message':'False_2','ID':'NULL'}
# 			return JsonResponse(data)
# 	else:
# 		return render(request, 'lms/login.html')
def home(request):
	return render(request, 'lms/home.html')

def signup(request):
	if request.method == 'POST':
		#print(request.POST['empID'])
		# q = {
		# 	'empID' : request.POST['empID'],
		# }
		# r = {
		# 	'username' : request.POST['username'],
		# 	'password1' : request.POST['password1'],
		# 	'password2' : request.POST['password2'],
		# }
		form = SignUpForm(request.POST)
		if Employee.objects.filter(empID=request.POST['empID']):
			form1 = SignUpForm()
			mssg = "Error : Employee ID already exists"
			return render(request, 'lms/signup.html', {
				'form': form1,
				'mssg': mssg
			})

		#profile_form = EmployeeForm(q)
		#print(q)
		#print(r)
		if form.is_valid():
			print("hello")
			form.save()
			#profile_form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			emplID = form.cleaned_data.get('empID')
			print(form.cleaned_data.get('first_name'))
			firstName = form.cleaned_data.get('first_name')
			print(firstName)
			email = form.cleaned_data.get('email')
			if form.cleaned_data.get('last_name'):
				lastName = form.cleaned_data.get('last_name')
			else:
				lastName = ''
			Employee.objects.create(author=user,firstName=firstName,lastName=lastName,empID=emplID,email=email)
			return redirect('/leave/home')
	else:
		form = SignUpForm()
	return render(request, 'lms/signup.html', {
		'form': form,
		'mssg': None
	})
			

@login_required
@csrf_exempt
def leave_application(request):
	   
		   
	if request.method=='POST':
		#form = CustomModelForm(request.POST)
		form = LeaveApplicationForm(request.POST)
		#print(form.is_valid())
		#print(request.POST['startDate'])
		if form.is_valid():
			#print("hrllo")
			#leave_input = form.save(commit=False)
			#print(post.empID)
			leave_input = form.cleaned_data
			start_date = leave_input['startDate']
			print(start_date)
			#print(start_date)
			end_date = leave_input['endDate']
			print(end_date)
			employee = Employee.objects.filter(author=request.user)
			#print(employee[0])
			emp_id = employee[0].empID
			leave_type =leave_input['leave']
			phone_number =employee[0].empID
			
			start_date_string= start_date
			#print(start_date_string.weekday())
			end_date_string=end_date
			dates=leave_utils.check_holidays(start_date_string,end_date_string)
			try:
				start_date_string=dates.get('start date')
				end_date_string=dates.get('end date')
			except:
				start_date_string= string_to_date(start_date)
				end_date_string=string_to_date(end_date)

			final_message=''
			
			# employee = PhoneNumber.objects.filter(
			# 		phoneNumber=phone_number).values('empID')
			if not employee:
				data={
				'user message':"Employee not found",
				'user unique_id':phone_number
				}
				message = data['user message']
				return render(request, 'lms/leave_result.html', {'message': message})
			emp_id=employee[0].empID
			
			
			

			"""Input validation"""
			is_valid = leave_utils.validate_input(emp_id,
				leave_type,start_date,end_date)
			case=is_valid.get('case')
			case1=is_valid.get('case1')
			message=is_valid.get('message')
			if case == 0 or case1==0:
				data={
				'user message':message
				}
				message = data['user message']
				return render(request, 'lms/leave_result.html', {'message': message})
			case=2
			if get_values.can_leave_be_applied(emp_id,start_date_string,end_date_string)==True and leave_type=='CASUAL LEAVE' and start_date_string.weekday()<5:
			#f=get_values.can_leave_be_applied(emp_id,start_date_string,end_date_string)
			#if f:
				data={
				'user message':"casual leave cannot be applied."
				}
				message = data['user message']
				return render(request, 'lms/leave_result.html', {'message': message})
			duration = float(leave_utils.calculate_duration(
				start_date_string,end_date_string))
			"""Fetching phone number and empID from that."""
			if get_values.can_el_be_applied(emp_id,start_date_string,end_date_string,duration)==False:
				data={
				'user message':"earn leave cannot be applied."
				}
				message = data['user message']
				return render(request, 'lms/leave_result.html', {'message': message})

			
			if (leave_type=='MATERNITY LEAVE') and (employee[0]['gender']=='Male'):
				data ={
				'user message':'You are not allowed to take this leave.',
				'user unique_id': phone_number
				}
				message = data['user message']
				return render(request, 'lms/leave_result.html', {'message': message})
			"""Fetching leave history from database"""
			instance_log = list(
					EmployeeLeaveLog.objects.filter(
					empID=emp_id).filter(date__gte=start_date_string).filter(date__lte=(end_date_string)).values())
			if not instance_log:
				case=2
			else:
				for i in range(0,len(instance_log)):
					"""Checking whether leave is taken or not by the user and Update leave """
					temp=(instance_log[i]['date']).strftime("%m/%d/%Y %H:%M:%S")
					start_date_str=(start_date_string.strftime("%m/%d/%Y %H:%M:%S"))
					end_date_str=(end_date_string.strftime("%m/%d/%Y %H:%M:%S"))

					if (instance_log[i]['leaveType']==leave_type) and ((
						start_date_str== temp)):
						case=0
						message='You have already applied for leave.'
						break
					
					elif(instance_log[i]['leaveType']!=leave_type) and ((
						start_date_str==temp )):
						case=1
						prev_leave = instance_log[i]['leaveType']
						emp=EmployeeLeaveLog.objects.get(empID=emp_id,date=start_date_string,leaveType=prev_leave)
						emp.delete()
						break
					else:
						case=2
						
			"""Data to bot if employee has already applied for leave"""
			if case==0 or case==3:
				data={
					'user message':message,
					'user unique_id':phone_number
				}	
				message = data['user message']
				return render(request, 'lms/leave_result.html', {'message': message})
			
			
			options = {
			   'CASUAL LEAVE' : get_values.cl,
			   'SICK LEAVE' : get_values.sl,
			   'VACATION LEAVE' :get_values.vl,
			   'EARN LEAVE' : get_values.el,
			   'MATERNITY LEAVE' : get_values.ml,
			   'WORK FROM HOME':get_values.wfh
			}
			if case==2 or case==1:
				leave_update=options.get(leave_type)
				info=leave_update(emp_id,duration)
				case1=info.get('case',None)
				team_list=get_values.get_team_mates(emp_id)
				
				if case1==3:
					data = {
					'user message':'Your request has been declined due to '
								+'less number of leaves in your account',
					'user unique_id' : phone_number,
					#'leaves left':leaves_left
						}
					#print(data['user message'])
					message = data['user message']
					message = data['user message']
					return render(request, 'lms/leave_result.html', {'message': message})
				if case ==2 :
					data = {
						'user message':info.get('message'),
						'user unique_id' : phone_number,
						}
				if case==1:
					data={
						'user message':'Your leave has been updated.',
						'user unique_id':phone_number,
						}
					''' Updating the database with previous leave status as false'''
					options1 = {
					   'CASUAL LEAVE' : get_values.ucl,
					   'SICK LEAVE' : get_values.usl,
					   'VACATION LEAVE' :get_values.uvl,
					   'EARN LEAVE' : get_values.uel,
					   'MATERNITY LEAVE' : get_values.uml,
					   'WORK FROM HOME':get_values.uwfh
					}
					update_leave=options1.get(prev_leave)
					update_leave(emp_id,duration)
					transaction_instance_update = EmployeeLeaveTransaction.objects.get(
						empID =emp_id,leave =prev_leave, 
						startDate =(start_date_string), endDate =(end_date_string), 
						duration =duration)
					transaction_instance_update.status=False
					transaction_instance_update.save()

			'''saving the application in datatbase'''
			if case==2 or case==1:
				employee = Employee.objects.get(empID=emp_id)
				employee1 = Employee.objects.get(empID=employee.managerID)
				manager_email=employee1.email
				subject = "Leave Application of "+str(emp_id)
				text =  str(employee.firstName) +" has applied for "+ leave_type.lower()+" from "+ str(start_date) + " to " + str(end_date)
				to_mail = [manager_email]
				email=EmailMessage(subject,text,"avionics1418@gmail.com",
					to_mail)
				email.send()

			if case1!=3:
				start_date_temp=(start_date_string)
				employee = Employee.objects.get(empID=emp_id)
				while start_date_temp <= end_date_string:
					log_instance = EmployeeLeaveLog(empID=employee,
						date=start_date_temp,leaveType=leave_type)
					log_instance.save()
					start_date_temp+=timedelta(days=1)
				
				lm_instance=EmployeeLeaveMaster.objects.get(empID=emp_id)
				leave_transaction=EmployeeLeaveTransaction(empID=employee,
					leave=leave_type,startDate=start_date_string,
					endDate=end_date_string,duration=duration,messageReceived=final_message,status=True)
				leave_transaction.save()
				#print(EmployeeLeaveTransaction.objects.filter(empID=emp_id).values())
			#return JsonResponse(data)
			message = data['user message']
			return render(request, 'lms/leave_result.html', {'message': message})

	else:		
		#form = CustomModelForm()
		form = LeaveApplicationForm()
	month = timezone.now().month
	year = timezone.now().year
	day = timezone.now().day
	print(month);
	print(year);
	print(day);
	return render(request, 'lms/leave_application.html', {'form': form,'month': month,'day':day,'year':year})
	'''
	except:
		data={
		'user message':"Something went wrong, please try again."
		}
		return JsonResponse(data)
	'''
						
'''
This function finds out whether a person on leave or not. Checks the datatbase
whether the peson has taken a leave today.
'''	
@login_required
@csrf_exempt
def find_person(request):
	try:
		if request.method=='POST':
			leave_input = json.loads(request.body)
			emp_id = leave_input['employee_id']
			name  = leave_input['name']
			user_unique_id=leave_input.get('user unique_id',None)
			info=get_values.get_multiple_empID_name(emp_id,name)
			message=info.get('message',None)
			if message==False:
				data={
				'user message':"Employee cannot be found. Please try again with a valid input.",
				'user unique_id':user_unique_id
				}
				return JsonResponse(data)
			emp_id=info.get('emp_id')
			final_name=[]
			final_name=info.get('names')
			transaction_instance=[]
			message=''
			today_string = datetime.now().date()
			today_date_string=today_string.strftime("%m/%d/%Y %H:%M:%S")

			if len(emp_id)>0 :
				for i in range(0,len(emp_id)):
					transaction_instance += list(
							EmployeeLeaveTransaction.objects.filter(
							empID=emp_id[i],startDate=today_string).values('startDate','endDate','empID'))
				if not transaction_instance:
					case=0
					for i in range(0,len(emp_id)):
						message+='You can find '+final_name[i]+' '+str(emp_id[i]) +' in the office today.\n'
					
				elif len(emp_id)==1:
					for i in range(0,len(transaction_instance)):
						startDate_string = ((transaction_instance[i]['startDate']).date()).strftime("%m/%d/%Y %H:%M:%S")  
						endDate_string = (transaction_instance[i]['endDate'].date()).strftime("%m/%d/%Y %H:%M:%S") 
						if today_date_string==startDate_string or today_string==endDate_string:
							case = 1
							message = final_name[0]+' '+ str(emp_id[0])+' is on leave today\n' 
							break
						else:
							case = 0
							message = 'You can find '+final_name[0]+' '+str(emp_id[0]) +' in the office today.\n'
				else:
					for j in range(0,len(emp_id)):
						for i in range(0,len(transaction_instance)):
							#print(transaction_instance[i])
							#print("in for loop") 
							startDate_string = transaction_instance[i]['startDate'].strftime("%m/%d/%Y %H:%M:%S")  
							endDate_string = transaction_instance[i]['endDate'].strftime("%m/%d/%Y %H:%M:%S")
						
							if (today_date_string==startDate_string or today_date_string==endDate_string) and (emp_id[j]==transaction_instance[i]['empID']):
								case = 1
								message+=str(final_name[j])+' '+str(emp_id[j])+ ' is on leave today.\n'
								break
							else:
								case = 0
								message+='You can find '+final_name[j]+' '+str(emp_id[j]) +' in the office today.\n'
				if case==1 :
					
					data = {
					'user message': message,
					'user unique_id': user_unique_id
					}
				elif case==0:
					
					data = {
					'user message': message,
					#'empID' : emp_id,
					'user unique_id': user_unique_id
					}
			return JsonResponse(data)
	except:
		data={
		'user message':"Something went wrong, please try again."
		}
		return JsonResponse(data)

@login_required
@csrf_exempt
def cancel_leave(request):
	try:		
		if request.method=='POST':

			form = CustomModelForm(request.POST)
			if form.is_valid():
				#print("hello")
				leave_input = form.save(commit=False)
				#print(post.empID)
				start_date = leave_input.startDate
				end_date = leave_input.endDate
				employee = Employee.objects.filter(author=request.user)
				print(employee[0])
				emp_id = employee[0].empID
				leave_type =leave_input.leave
				phone_number =employee[0].empID
				message = ''			
				start_date_string= start_date
				end_date_string=end_date

				#leave_input = json.loads(request.body)
				#emp_id = leave_input.get('employee_id',None)
				#start_date = leave_input.get('current end date',None)
				#end_date=leave_input.get('initial end date',None)
				#phone_number=leave_input.get('user unique_id',None)
				#message=leave_input.get('message',None)	
				#leave_type = leave_input.get('leave type',None)
				#start_date_string = string_to_date(start_date)
				#end_date_string = string_to_date(end_date)
				duration = leave_utils.calculate_duration(
						start_date_string,end_date_string)
				duration=float(duration)
				print(duration)
				"""Fetching phone number and empID from that."""
				#if emp_id=="" or emp_id is None:

					#employee = PhoneNumber.objects.filter(
							#phoneNumber=phone_number).values('empID')
					
				if not employee:
					data={
					'user message':'Fail_2',#"Employee not found",
					'user unique_id':phone_number
					}
					return JsonResponse(data)
				#emp_id = employee[0]['empID']

				employee = Employee.objects.get(empID=emp_id)
				manager = employee.managerID
				leave_master_instance = EmployeeLeaveMaster.objects.get(empID=emp_id)
				instance_log = list(
							EmployeeLeaveLog.objects.filter(
							empID=emp_id).values())
				if not instance_log:
					case=1
				else:
					for i in range(0,len(instance_log)):
						temp=(instance_log[i]['date']).strftime("%m/%d/%Y %H:%M:%S")
						start_temp = start_date_string.strftime("%m/%d/%Y %H:%M:%S")
						end_temp=end_date_string.strftime("%m/%d/%Y %H:%M:%S")
						if (temp== start_temp):
							EmployeeLeaveLog.objects.filter(empID=employee,
								date=start_date_string).delete()
							case=0
							break		
						else:
							case=1
				#print(case,"*********")
				if case == 0:
					if leave_type=='CASUAL LEAVE':
						leave_master_instance.casualLeavesLeft+=duration
						leave_master_instance.save()
					elif leave_type=='SICK LEAVE':
						leave_master_instance.sickLeavesLeft+=duration
						leave_master_instance.save()
					elif leave_type=='VACATION LEAVE':
						leave_master_instance.VacationLeavesLeft+=duration
						leave_master_instance.save()
					elif leave_type == 'EARN LEAVE':
						leave_master_instance.earnLeavesLeft+=duration
						leave_master_instance.save()
					data = {
						'status':'Success' ,
						'user unique_id':phone_number,
					}

					EmployeeLeaveTransaction.objects.filter(empID=employee,
								startDate=start_date_string).delete()
					lm_instance=EmployeeLeaveMaster.objects.get(empID=emp_id)
					transaction_instance = EmployeeLeaveTransaction(empID=employee,
						startDate=start_date_string,endDate=end_date_string,
						duration=duration,messageReceived=message,status=False)
					transaction_instance.save()
					employee = Employee.objects.get(empID=emp_id)
					employee1 = Employee.objects.get(empID=employee.managerID)
					employee_email=employee1.email
					subject = "Leave Application of "+str(emp_id)
					text =  str(employee.firstName) +" has cancelled leave from "+ str(start_date) + " to " + str(end_date)
					to_mail = [employee_email]
					return JsonResponse(data)
					
					email=EmailMessage(subject,text,"avionics1418@gmail.com",
						to_mail)
					email.send()
					
				else:
					data = {
						'status':'Fail_1', #You have not applied for leave yet.',
						'user unique_id':phone_number,
						
					}
				return JsonResponse(data)
		else:
			form = CustomModelForm()
			return render(request, 'lms/cancel_leave.html', {'form': form})

	except:
		data={
			'status':"Fail_3" #Something went wrong with the API
		}
		return JsonResponse(data)

@login_required
@csrf_exempt
def leave_balance_report1(request):
	#try:
	#if request.method=='POST':
		#leave_input = json.loads(request.body)
		#print(leave_input)
		#emp_ids = (leave_input.get('employee_id',None))
		#print(emp_ids)
		employee = Employee.objects.filter(author=request.user)
		emp_ids = "None"
		#phone_number=leave_input.get('user unique_id',None)
		phone_number = employee[0].empID
		#names=(leave_input.get('name',None))
		names = "None"
		#employee = PhoneNumber.objects.filter(
				#phoneNumber=phone_number).values('empID')

		

		
		if not employee:
			data={
			'user message':"Employee not found",
			'user unique_id':phone_number
			}
			return JsonResponse(data)
		if (len(emp_ids)==1 or not emp_ids) and (u'None' not in emp_ids):
			try:
				employees=Employee.objects.get(empID=emp_ids[0])
			except:
				data={
				'user message':"Employee not found.",
				'user unique_id':phone_number
				}
				return JsonResponse(data)
		report=list()
		leave_master=[]
		access = False
		temp=0
		info=get_values.get_multiple_empID_name(emp_ids,names)
		final_name=[]
		emp_ids=info.get('emp_id')
		final_name=info.get('names')
		names=info.get('name')
		if (not emp_ids) and (not names):
			access=True
		else:
			authorized=get_values.is_authorized(phone_number,emp_ids,final_name)
			access=authorized.get('access')
			emp_ids=authorized.get('emp_ids')
			final_name=authorized.get('names')
		print(access)

		if access==False:
			data = {
				'user message':'You are not authorised to view the'+
				' leave balance report.',
				'user unique_id':phone_number,
			}
			return JsonResponse(data)
		

		if access == True:
			if ((not names) and (not emp_ids)) :
				emp_ids_instance=PhoneNumber.objects.filter(
						phoneNumber=phone_number).values()
				emp_ids=list((emp_ids_instance[0]['empID_id']).split(","))
			if len(emp_ids)==1:
				try:
					leave_master+=list(EmployeeLeaveMaster.objects.filter(empID=emp_ids[0]['empID']).values('empID','casualLeavesLeft','sickLeavesLeft',
							'VacationLeavesLeft','earnLeavesLeft'))
				except:
					leave_master+=list(EmployeeLeaveMaster.objects.filter(empID=emp_ids[0]).values('empID','casualLeavesLeft','sickLeavesLeft',
							'VacationLeavesLeft','earnLeavesLeft'))

			else:
				for i in range(0,len(emp_ids)):
					try:
						leave_master += list(EmployeeLeaveMaster.objects.filter(
							empID=emp_ids[i]['empID']).values(
							'empID','casualLeavesLeft','sickLeavesLeft',
							'VacationLeavesLeft','earnLeavesLeft'))
					except:
						leave_master += list(EmployeeLeaveMaster.objects.filter(
							empID=emp_ids[i]).values(
							'empID','casualLeavesLeft','sickLeavesLeft',
							'VacationLeavesLeft','earnLeavesLeft'))
		
			
			data={
					'user message':'Here are the leave balances as you requested.'+ str(leave_master),
					'user unique_id':phone_number,
					#'leave_balances':leave_master,
				}
			return JsonResponse(data)
	#except:
		#data={
		#'user message':"Something went wrong, please try again."
		#}
		#return JsonResponse(data)

@login_required
@csrf_exempt
def leave_balance_report(request):
	#try:
	#if request.method=='POST':
		#leave_input = json.loads(request.body)
		#print(leave_input)
		#emp_ids = (leave_input.get('employee_id',None))
		#print(emp_ids)
		employee = Employee.objects.filter(author=request.user)
		emp_ids = "None"
		#phone_number=leave_input.get('user unique_id',None)
		phone_number = employee[0].empID
		#names=(leave_input.get('name',None))
		names = "None"
		#employee = PhoneNumber.objects.filter(
				#phoneNumber=phone_number).values('empID')

		

		
		#EmployeeLeaveMaster.objects.filter(empID=emp_ids[0]['empID']).values('empID','casualLeavesLeft','sickLeavesLeft',
		#					'VacationLeavesLeft','earnLeavesLeft'))
		emp = EmployeeLeaveMaster.objects.filter(empID=employee[0].empID)
		casualLeavesLeft = emp.values('casualLeavesLeft')[0]['casualLeavesLeft']
		sickLeavesLeft = emp.values('sickLeavesLeft')[0]['sickLeavesLeft']
		VacationLeavesLeft = emp.values('VacationLeavesLeft')[0]['VacationLeavesLeft']
		earnLeavesLeft = emp.values('earnLeavesLeft')[0]['earnLeavesLeft']
		print(casualLeavesLeft)
		return render(request, 'lms/leave_balance.html', {'casualLeavesLeft':casualLeavesLeft,'sickLeavesLeft':sickLeavesLeft,
															'VacationLeavesLeft':VacationLeavesLeft, 'earnLeavesLeft':earnLeavesLeft})	
			
	#except:
		#data={
		#'user message':"Something went wrong, please try again."
		#}
		#return JsonResponse(data)

@login_required
@csrf_exempt
def leave_history_report1(request):
		if request.method=='POST':
			leave_input = request.POST
			#emp_id = (leave_input['employee_id'])
			#phone_number=leave_input['user unique_id']
			#start_date=leave_input['start date']
			#end_date=leave_input['end date']
			#name=(leave_input['name'])
			case = 1
			#message=leave_input.get('message',None)
			#employee = PhoneNumber.objects.filter(
					#phoneNumber=phone_number).values('empID')
			employee = Employee.objects.filter(author=request.user)
			emp_id = "None"
			phone_number = employee[0].empID
			start_date = leave_input['startDate']
			end_date = leave_input['endDate']
			#end_date = leave_input.endDate
			name = "None"
			message = ''

			if not employee:
				data={
				'user message':"Fail_2" ,#Employee not found",
				'user unique_id':phone_number
				}
				return JsonResponse(data)
			if (len(emp_id)==1 or not emp_id) and (u'None' not in emp_id):
				try:
					employees=Employee.objects.get(empID=emp_ids[0])
				except:
					data={
					'user message':"Fail_2",#"Employee not found.",
					'user unique_id':phone_number
					}
					return JsonResponse(data)
			report=[]
			leave_transaction=[]
			leave_master=[]
			info=get_values.get_multiple_empID_name(emp_id,name)
			print(info)
			emp_id=info.get('emp_id')
			
			final_name=info.get('names')
			name=info.get('name')
			if (not emp_id) and (not name):
				access=True
			else:
				authorized=get_values.is_authorized(phone_number,emp_id,final_name)
				access=authorized.get('access')
				
				emp_ids=authorized.get('emp_ids')
				final_name=authorized.get('names')
			print(access)
			if access == True:
				print("hello")
				if (not emp_id) and (not name):
					emp_id=list(PhoneNumber.objects.filter(
						phoneNumber=phone_number).values('empID'))
					emp_id=list((emp_id[0]['empID']).split(','))
				start_object = string_to_date(start_date)
				end_object=string_to_date(end_date)
				st=start_object
				i=0	
				start_temp=deepcopy(start_date)
				start_temp=parser.parse(start_temp)
				start_temp=datetime(start_temp.year,start_temp.month,start_temp.day)
				if len(emp_id)==1:
					leave_transaction=list(EmployeeLeaveTransaction.objects.filter(
						empID=emp_id[0]).filter(startDate__gte=start_temp).values('empID_id','leave','startDate','endDate','duration','status','messageReceived'))
					if leave_transaction:

						leave_transaction1=EmployeeLeaveTransaction.objects.get(empID=emp_id[0],startDate=leave_transaction[0]['startDate'],endDate=leave_transaction[0]['endDate'],duration=leave_transaction[0]['duration'],status=leave_transaction[0]['status'])
					
						
					else:
						case=0

					for i in range(0,len(leave_transaction)):
						start=((leave_transaction[i]['startDate'])).date()
						end=((leave_transaction[i]['endDate'])).date()
						if (start>=start_object.date(
							) and start <=end_object.date(
							)) and(end>=start_object.date(
							) and end<=end_object.date()) :
							report.append(leave_transaction[i])
							

				else:
					for i in range(0,len(emp_id)):
						leave_transaction = list(
							EmployeeLeaveTransaction.objects.filter(
								empID=emp_id[i]).filter(startDate__gte=start_temp).values('empID_id','leave','startDate','endDate','duration','status','messageReceived'))
						if leave_transaction:

							leave_transaction1=EmployeeLeaveTransaction.objects.get(empID=emp_id[0],startDate=leave_transaction[0]['startDate'],endDate=leave_transaction[0]['endDate'],duration=leave_transaction[0]['duration'],status=leave_transaction[0]['status'])
						
							for j in range(0,len(leavesLeft)):
								if leave_transaction1.leave[i][0].lower()==leavesLeft[j][0]:
									t=leavesLeft[j]
									leave_transaction=list(EmployeeLeaveTransaction.objects.filter(empID=emp_id[i]).filter(startDate__gte=start_temp).values('empID_id','leave','startDate','endDate','duration','status','messageReceived',t))
									break
								else:
									leave_transaction=list(EmployeeLeaveTransaction.objects.filter(empID=emp_id[i]).filter(startDate__gte=start_temp).values('empID_id','leave','startDate','endDate','duration','status','messageReceived'))


							for j in range(0,len(leave_transaction)):
								if len(leave_transaction)==0:
									break
								else:
									if (leave_transaction[j][
										'startDate']>=start_object.date(
										) and leave_transaction[j][
										'startDate'] <= end_object.date()) and (
										leave_transaction[j][
										'endDate']>=start_object.date(
										) and leave_transaction[
										j]['endDate']<= end_object.date()) :
										report.append(leave_transaction[j])
						else:
							case=0
				print (report)
				if report and case!=0:
					df=pd.DataFrame(report)
					try:
						df.columns=['Duration','Employee ID','End Date','Leave Type','Message Received','Start Date', 'Status']
						df = df[['Employee ID','Leave Type','Duration','Start Date','End Date','Status','Message Received']]
					except:
						df.columns=['Duration','Employee ID','End Date','Leave Type','Message Rceived','Start Date', 'Status']
						df = df[['Employee ID','Leave Type','Duration','Start Date','End Date','Status','Leaves Left','Message Received']]
					
					df.to_csv("spreadsheet.csv")
					employee_phone = PhoneNumber.objects.get(phoneNumber=phone_number)
					employee_id=employee_phone.empID.empID
					employee = Employee.objects.get(empID=employee_id)
					employee_email=employee.email
					subject = "Leave History Report"
					text =  "Leave history report from "+str(start_date)+ " to " + str(end_date)
					to_mail = [employee.email]
					email=EmailMessage(subject,text,"avionics1418@gmail.com",
						to_mail)
					file=open('spreadsheet.csv','r') 
					email.attach('report.csv',file.read(),'text/plain')
					email.send()
					message="Success"
				else:
					message="Fail_1" #No leave data could be found."
				data={
						'user message':message,
						'user unique_id':phone_number,
						
					}
				return JsonResponse(data)
			else:
				data={
				'user message':message,
				'user unique_id':phone_number

				}
				return JsonResponse(data)
		else:
			return render(request, 'lms/leave_history.html')

@login_required
def leave_history_report(request):
	if request.method=='POST':
		#form = CustomModelForm(request.POST)
		#form = LeaveApplicationForm(request.POST)
		#print(form.is_valid())
		startDate = request.POST['startDate']
		print(startDate)
		endDate = request.POST['endDate']
		to_delete = EmployeeLeaveTransaction.objects.filter(startDate=startDate,endDate=endDate)
		print(to_delete)
		employee = Employee.objects.filter(author=request.user)
		emp_id = employee[0].empID
		month = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'] 
		list_of_leaves = EmployeeLeaveTransaction.objects.filter(empID=emp_id)
		
		#if form.is_valid():
			#print("hrllo")
			#leave_input = form.save(commit=False)
			#print(post.empID)
			#leave_input = form.cleaned_data
			#start_date = leave_input['startDate']
			#end_date = leave_input['endDate']
			#print(request.POST['start_date'])
	else:
		employee = Employee.objects.filter(author=request.user)
		emp_id = employee[0].empID
		month = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'] 
		list_of_leaves = EmployeeLeaveTransaction.objects.filter(empID=emp_id)
	return render(request, 'lms/leave_history.html', {'list_of_leaves':list_of_leaves,'month':month})


@login_required
@csrf_exempt
def add_employee(request):     
	if request.method=='POST':
		employee_data= json.loads(request.body)
		employee_id = employee_data.get('employeeID',None)
		first_name = employee_data.get('firstName',None)
		last_name = employee_data.get('lastName',None)
		user_id =employee_data.get('userID',None)
		phone_number =employee_data.get('mobile',None)
		email=employee_data.get('email',None)
		present_address=employee_data.get('currentAddress',None)
		permanent_address=employee_data.get('permanentAddress',None)
		manager_id=employee_data.get('managerID',None)
		gender = employee_data.get('gender',None)
		designation = employee_data.get('designation',None)
		joining_date = employee_data.get('joiningDate',None)
		#manager=list(manager.split(' '))

		message='Employee has been added successfully.'
		try:
			employee = Employee(empID=employee_id,empUniqueID=user_id,firstName=first_name,lastName=last_name,email=email,joiningDate=joining_date,designation=designation,managerID=manager_id,gender=gender)	
			employee.save()
			emp=Employee.objects.get(empID=employee_id)
			employee_address=EmployeeAddress(empID=emp,permanentAddress=permanent_address,presentAddress=present_address)
			employee_address.save()
			employee_phone=PhoneNumber(empID=emp,phoneNumber=phone_number)
			employee_phone.save()
			emp_address=EmployeeAddress.objects.get(empID=employee_id)
			emp_phone=PhoneNumber.objects.get(empID=employee_id)
			employee.address=emp_address
			employee.phoneNumber=emp_phone
			employee.save()
			return HttpResponse(status = 200)
		except:
			message='Problem occured while adding employee. Please try again.'
			return HttpResponse(status = 400)

@login_required
@csrf_exempt
def adjust_leaves(request):
	if request.method=='POST':
		leaves_input=json.loads(request.body)
		casual_leaves=leaves_input.get('casual leaves',None)
		sick_leaves=leaves_input.get('sick leaves',None)
		Vacation_leaves=leaves_input.get('Vacation leaves',None)
		earn_leaves=leaves_input.get('earn leaves',None)
		maternity_leaves=leaves_input.get('maternity leaves',None)
		message='Leaves has been updated successfully'
		try:
			casual_leave = Leave.objects.get(leaveName='CASUAL LEAVE')
			sick_leave = Leave.objects.get(leaveName='SICK LEAVE')
			Vacation_leave = Leave.objects.get(leaveName='VACATION LEAVE')
			earn_leave = Leave.objects.get(leaveName='EARN LEAVE')
			maternity_leave = Leave.objects.get(leaveName='MATERNITY LEAVE')
			casual_leave.totalSanctioned=casual_leaves
			casual_leave.save()
			sick_leave.totalSanctioned=sick_leaves
			sick_leave.save()
			Vacation_leave.totalSanctioned=Vacation_leaves
			Vacation_leave.save()
			earn_leave.totalSanctioned=earn_leaves
			earn_leave.save()
			maternity_leave.totalSanctioned=maternity_leaves
			maternity_leave.save()
		except:
			message='Problem occured during updating sanctioned leaves. Please try again.'
		data={
		'message':message,
		}
		return JsonResponse(data)

@login_required
@csrf_exempt
def update_holidays(request):
	if request.method=='POST':
		holiday_input = json.loads(request.body)
		#holiday_input=ast.literal_eval(request.body)
		holiday_list=holiday_input.get('holiday list',None)
		holiday_list=holiday_list.split(",")
		holiday_list = [n.strip() for n in holiday_list]
		holiday_list = [n.encode('UTF-8') for n in holiday_list]
		if not holiday_list:
			message='Holiday list is not updated. Please try again.'
		else:
			message='Holiday list is updated.'
		data={
		'message':message
		}
		return JsonResponse(data)



