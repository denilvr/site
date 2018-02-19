from leave.models import (Employee,
	EmployeeProject,
	EmployeeLeaveLog,
	EmployeeLeaveMaster,
	EmployeeLeaveTransaction,
	PhoneNumber
	)
from datetime import datetime,timedelta
import leave.leave_utils 

def get_empid(x):
	message=""
	try:
		phone_instance = PhoneNumber.objects.get(phoneNumber=x)
		emp_id=phone_instance.empID
	except:
		message="Employee not found"
	data={
	'empid':emp_id,
	message:message
	}
	return data



# define the function blocks
def cl(emp_id,duration):
	leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
	leaves_left = leave_master.casualLeavesLeft
	if duration>leaves_left:
		case=3
		data={
		'case':case,
		'message':'leaves are less.'
		}
	else:
		leave_master.casualLeavesLeft-=duration
		leave_master.save()
		data={
		'message':'your leave request has been accepted'
		}
	return data

def vl(emp_id,duration):
	leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
	leaves_left = leave_master.VacationLeavesLeft
	if duration>leaves_left:
		case=3
		data={
		'case':case,
		'message':'leaves are less.'
		}
	else:
		leave_master.VacationLeavesLeft-=duration
		leave_master.save()
		data={
		'message':'your leave request has been accepted'
		}
	return data


def sl(emp_id,duration):
	leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
	leaves_left = leave_master.sickLeavesLeft
	if duration>2:
		message='Your leave request has been accepted. Please make sure you submit your medical certificate to your manager on your day back to office.'
	else:
		message='your leave request has been accepted'
	if duration>leaves_left:
		case=3
		data={
		'case':case,
		'message':message
		}
	else:
		leave_master.sickLeavesLeft-=duration
		leave_master.save()
		data={
		'message':message
		}
	
	return data
'''
def al(emp_id,duration):
	leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
	leaves_left = leave_master.vacationLeavesLeft
	if leaves_left<-5:
		case=3
		data={
		'case':case,
		'message':'Your leave request has been accepted.'
		}
	else:
		leave_master.vacationLeavesLeft-=duration
		leave_master.save()
		data={
		'message':'Your leave request has been accepted.'
		}
	return data
'''

def el(emp_id,duration):
	leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
	leaves_left = leave_master.earnLeavesLeft
	message='Your leave request has been accepted. Please make sure you take your supervisor permission for this leave application. If your supervisor do not accept the leave application make sure that you cancel this leave.'
	if duration>leaves_left:
		case=3
		data={
		'case':case,
		'message':message
		}
	else:
		leave_master.earnLeavesLeft-=duration
		leave_master.save()
		data={
		'message':message
		}
	
	return data


def ml(emp_id,duration):
	leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
	leave_master.maternityLeavesLeft=0
	leave_master.save()
	data={
	'case':case,
	'message':'Your leave request has been accepted. Please make sure you take your supervisor permission for this leave application. If your supervisor do not accept the leave application make sure that you cancel this leave.'
	}
	return data

def wfh(emp_id,duration):
	leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
	leave_master.work_from_home_availed +=duration
	leave_master.save()
	data={
	'case':case,
	'message':'Your request has been accepted.'
	}
	return data


def ucl(emp_id,duration):
    leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
    leave_master.casualLeavesLeft +=duration
    leave_master.save()
def uvl(emp_id,duration):
    leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
    leave_master.VacationLeavesLeft +=duration
    leave_master.save()

def usl(emp_id,duration):
    leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
    leave_master.sickLeavesLeft +=duration
    leave_master.save()
'''
def ual(emp_id,duration):
    leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
    leave_master.vacationLeavesLeft +=duration
    leave_master.save()
'''
def uel(emp_id,duration):
    leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
    leave_master.earnLeavesLeft +=duration
    leave_master.save()

def uml(emp_id,duration):
    leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
    leave_master.maternityLeavesLeft +=duration
    leave_master.save()
def uwfh(emp_id,duration):
    leave_master = EmployeeLeaveMaster.objects.get(empID=emp_id)
    leave_master.work_from_home_availed -=duration
    leave_master.save()

def can_cl_be_applied(emp_id,start,end,leave):
	if start.weekday()==5 or end.weekday()==5:
		log_instance = list(EmployeeLeaveLog.objects.filter(empID=emp_id,date__gte=start-timedelta(days=1),date__lte=end+timedelta(days=3)).values())
	elif start.weekday()==0 or end.weekday()==0:
		log_instance = list(EmployeeLeaveLog.objects.filter(empID=emp_id,date__gte=start-timedelta(days=3),date__lte=end+timedelta(days=1)).values())
	else:
		log_instance = list(EmployeeLeaveLog.objects.filter(empID=emp_id,date__gte=start-timedelta(days=1),date__lte=end+timedelta(days=1)).values())
	c=False
	if not log_instance:
		c=True
	else:
		for i in log_instance:
			temp=(i['date']).strftime("%m/%d/%Y %H:%M:%S")
			try:

				start=(start.strftime("%m/%d/%Y %H:%M:%S"))
				end=(end.strftime("%m/%d/%Y %H:%M:%S"))
			except:
				pass
			if (i['leaveType']=='CASUAL LEAVE' and leave!='CASUAL LEAVE'):
				if temp==start or temp==end:
					c=True 
				else:
					c=False
				break
			elif leave=='CASUAL LEAVE' and i['leaveType']!='CASUAL LEAVE':
				if temp==start or temp==end:
					c=True 
				else:
					c=False
				break
			else:
				c=True
	return c

def can_cl_be_applied1(emp_id,start,end):
	cl=list(EmployeeLeaveLog.objects.filter(empID=emp_id).values())
	if start.weekday()==2:
		if (start-timedelta(days=1) in cl and start+timedelta(days=1) in cl) or (start-timedelta(days=1) in cl and start-timedelta(days=2) in cl) or (start+timedelta(days=1) in cl and start+timedelta(days=2) in cl):
			c=False
		else:
			c=True
	elif start.weekday()==1:
		if (start-timedelta(days=1) in cl and start+timedelta(days=1) in cl) or (start-timedelta(days=1) in cl and start-timedelta(days=4) in cl) or (start+timedelta(days=1) in cl and start+timedelta(days=2) in cl):
			c=False
		else:
			c=True
	elif start.weekday()==0:
		if (start-timedelta(days=3) in cl and start+timedelta(days=1) in cl) or (start-timedelta(days=3) in cl and start-timedelta(days=4) in cl) or (start+timedelta(days=1) in cl and start+timedelta(days=2) in cl):
			c=False
		else:
			c=True
	elif start.weekday()==3:
		if (start-timedelta(days=1) in cl and start+timedelta(days=1) in cl) or (start-timedelta(days=1) in cl and start-timedelta(days=2) in cl) or (start+timedelta(days=1) in cl and start+timedelta(days=4) in cl):
			c=False
		else:
			c=True
	elif start.weekday()==4:
		if (start-timedelta(days=1) in cl and start+timedelta(days=3) in cl) or (start-timedelta(days=1) in cl and start-timedelta(days=2) in cl) or (start+timedelta(days=3) in cl and start+timedelta(days=4) in cl):
			c=False
		else:
			c=True
	return c

def get_multiple_empID_name(emp_id,name):
	names=[]
	message=True
	if u'None' in emp_id or (u'me' in emp_id) :
		emp_id = []
	else:
		emp_id = list(emp_id.split(','))
	if u'None' in name or (u'me' in name):
		name = []
	else:
		name = list(name.split(','))


	if len(name)>0:
		for i in range(0,len(name)):
			try:
				employee = list(Employee.objects.filter(firstName=name[i].title()).values('empID'))
				if not employee:
					employee = list(Employee.objects.filter(lastName=name[i].title()).values('empID'))
				
			except:
				message=False

			if len(employee)==1:

				emp_id+=list(employee[0]['empID'].split(','))
			else:
				for i in range(0,len(employee)):
					emp_id +=list((employee[i]['empID']).split(','))
	for i in range(0,len(emp_id)):
		names.append((Employee.objects.get(empID=emp_id[i])).firstName)
	#if not employee:
	try:
		if not employee:
			message=False
	except:
		pass
	
	data={
	'emp_id':emp_id,
	'names':names,
	'name':name,
	'message':message
	}

	return data
def is_authorized(phone_number,emp_ids,names):
	user_id_instance = PhoneNumber.objects.get(phoneNumber=phone_number)
	user_id = user_id_instance.empID
	print(user_id.empID)
	user_instance = Employee.objects.get(empID=user_id.empID)
	user_name = user_instance.firstName
	temp=[]
	if leave.leave_utils.is_HR(user_id.empID):
		access = True
	elif ((not emp_ids) and (not names) ) and (not temp):
		access = True
	else:
		for i in range(0,len(emp_ids)):
			try:
				if ((leave.leave_utils.is_manager(user_id,emp_ids[i]))==False):
					temp.append(emp_ids[i])
					emp_ids.remove(emp_ids[i])
					names.remove(names[i])
				else:
					pass
			except:
				if ((leave.leave_utils.is_manager(user_id,emp_ids[i-1]))==False):
					temp.append(emp_ids[i-1])
					emp_ids.remove(emp_ids[i-1])
					names.remove(names[i-1])
				else:
					pass
		if not emp_ids and (not temp==False):
			access=False
		for i in range(0,len(emp_ids)):
			if ((leave.leave_utils.is_manager(user_id,emp_ids[i]))):
				access=True
			else:
				access=False
				break

	data={
	'emp_ids':emp_ids,
	'access':access,
	'names':names
	}
	return data

def get_team_mates(emp_id):
	user_project=list(EmployeeProject.objects.filter(empID=emp_id).values())
	team=[]
	team_list=""
	for i in range(0,len(user_project)):
		team+=list((EmployeeProject.objects.filter(projectID=user_project[i]['projectID_id']).values('empID')))
	team=[x for x in team if not (emp_id == x.get('empID'))]
	for i in team:
		team_list+=str(i['empID'])+","
	return team_list

def can_leave_be_applied(emp_id,start,end):
	if(start.weekday())==0:
		day_before_yesterday=start-timedelta(days=4)
		yesterday=start-timedelta(days=3)
		tomorrow=start+timedelta(days=1)
		day_after_tomorrow=start+timedelta(days=2)
	elif(start.weekday())==1:
		day_before_yesterday=start-timedelta(days=4)
		yesterday=start-timedelta(days=1)
		tomorrow=start+timedelta(days=1)
		day_after_tomorrow=start+timedelta(days=2)
	elif(start.weekday())==2:
		day_before_yesterday=start-timedelta(days=2)
		yesterday=start-timedelta(days=1)
		tomorrow=start+timedelta(days=1)
		day_after_tomorrow=start+timedelta(days=2)
	elif(start.weekday())==3:
		day_before_yesterday=start-timedelta(days=2)
		yesterday=start-timedelta(days=1)
		tomorrow=start+timedelta(days=1)
		day_after_tomorrow=start+timedelta(days=4)
	elif(start.weekday())==4:
		day_before_yesterday=start-timedelta(days=2)
		yesterday=start-timedelta(days=1)
		tomorrow=start+timedelta(days=3)
		day_after_tomorrow=start+timedelta(days=4)
	
	day_before_yesterday_s= (day_before_yesterday).strftime("%m/%d/%Y %H:%M:%S")
	yesterday_s=(yesterday).strftime("%m/%d/%Y %H:%M:%S")
	tomorrow_s=(tomorrow).strftime("%m/%d/%Y %H:%M:%S")
	day_after_tomorrow_s=(day_after_tomorrow).strftime("%m/%d/%Y %H:%M:%S")

	lg=list(EmployeeLeaveLog.objects.filter(empID=emp_id).values())
	temp=[]

	for i in range(0,len(lg)):
		temp+=list((lg[i]['date']).strftime("%m/%d/%Y %H:%M:%S").split(","))

	if (yesterday_s in temp and tomorrow_s in temp)	 or (day_before_yesterday_s in temp and yesterday_s in temp) or (tomorrow_s in temp and day_after_tomorrow_s in temp):
		return True
	else:
		return False	 

def can_el_be_applied(emp_id,start,end,duration):
	elt=EmployeeLeaveTransaction.objects.filter(empID=8587).order_by('startDate')[:5]
	temp=[]
	d=0.0
	d=duration
	c=True
	for i in range(0,len(elt)):
		#print(elt[i].startDate)
		temp+=list((elt[i].startDate).strftime("%m/%d/%Y %H:%M:%S").split(","))
	if(start.weekday())==0:
		yesterday=start-timedelta(days=3)
	else:
		yesterday=start-timedelta(days=1)
	if(start.weekday()==4):
		tomorrow=start+timedelta(days=3)
	else:
		tomorrow=start+timedelta(days=1)

	ts=tomorrow.strftime("%m/%d/%Y %H:%M:%S")
	ys=yesterday.strftime("%m/%d/%Y %H:%M:%S")
	for i in range(0,len(elt)):
		if elt[i].leave=='EARN LEAVE' and ((ys in temp or ts in temp) or (leave.leave_utils.is_holiday((tomorrow.date()).strftime("%Y-%m-%d")) or leave_utils.is_holiday((tomorrow.date()).strftime("%Y-%m-%d")))):
			d+=elt[i].duration
			if d>=5:
				c=False
				break
	return c








