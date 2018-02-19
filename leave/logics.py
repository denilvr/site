from leave.models import *
from import datetime
from datetime import date,timedelta

def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def calculate_duration(startDate, endDate):
	daygenerator = (startDate + timedelta(x + 1) for x in range((endDate - startDate).days))
	duration = sum(1 for day in daygenerator if day.weekday() < 5)
	return duration



def update_leave_master(empID, leaveType, startDate, endDate):
	leave_instance = Leave.objects.get(leaveName=leaveType)
	employee_instance = Employee.objects.get(empID=empID)
	joining_date = employee_instance.joiningDate.month
	leave_type = leave_instance.totalSanctioned
	leave_master_instance = EmployeeLeaveMaster.objects.get(empID=empID)
	transaction_instance = EmployeeLeaveTransaction.objects.get(empID=empID)
	
	if leaveType == 'CASUAL LEAVE'
		leave_master_instance.clLeft = leave_master_instance.clLeft-transaction_instance.duration 
		leave_master_instance.save()
	if leaveType == 'SICK LEAVE'
		leave_master_instance.slLeft = leave_master_instance.slLeft-transaction_instance.duration 
		leave_master_instance.save()
	if leaveType == 'VACATION LEAVE'
		leave_master_instance.vlLeft = leave_master_instance.vlLeft-transaction_instance.duration 
		leave_master_instance.save()
	if leaveType == 'EARN LEAVE'
		leave_master_instance.elLeft = leave_master_instance.elLeft-transaction_instance.duration 
		leave_master_instance.save()
		
def validate_input(leaveType,startDate,endDate):
	d=calculate_duration(startDate,endDate)
	if leaveType== 'CASUAL LEAVE' or 'SICK LEAVE':
		return 1
	else 
		return 0
	if leave== 'EARN LEAVE':
		return 1
	else 
		return 0

def update_leave(empID,startDate,endDate):
	log_instance = EmployeeLeaveLog.objects.get(empID=empID)
	transaction_instance = EmployeeLeaveTransaction.objects.get(empID=empID)
	leave_master_instance = EmployeeLeaveMaster.objects.get(empID=empID)
	t=0
	i=log_instance.startDate.strftime("%Y-%m-%d")
	d = calculate_duration(startDate,endDate)
	s = startDate.strftime("%Y-%m-%d")
	es = transaction_instance.startDate.strftime("%Y-%m-%d")
	for s in date_range(startDate,endDate) :
		for es in date_range(startDate,endDate):
			EmployeeLeaveLog.objects.filter(startDate=startDate).delete()
			transaction_instance.duration = transaction_instance.duration-1
			if leave == 'CASUAL LEAVE'
				leave_master_instance.clLeft = leave_master_instance.clLeft+1 
				leave_master_instance.save()
			if leave == 'SICK LEAVE'
				leave_master_instance.slLeft = leave_master_instance.slLeft+1
				leave_master_instance.save()
			if leave == 'VACATION LEAVE'
				leave_master_instance.vlLeft = leave_master_instance.vlLeft+1
				leave_master_instance.save()
			if leave == 'EARN LEAVE'
				leave_master_instance.elLeft = leave_master_instance.elLeft+1
				leave_master_instance.save()
			es=es.timdelta(t+1)
		s=s.timdelta(t+1)
				
def is_present(empID):
	transaction_instance = EmployeeLeaveTransaction.objects.get(empID=empID)
	e = transaction_instance.startDate.strftime("%Y-%m-%d")
	t=0
	for e in date_range(transaction_instance.startDate,transaction_instance.endDate)
		if transaction_instance.startDate.strftime("%Y-%m-%d") == datetime.today().date().strftime("%Y-%m-%d")
			r = 0
		else 
			r = 1
		e = e.timedelta(t+1)
	return r
	
def is_manager(empID):
	employee_instance = Employee.objects.filter(managerID=empID)	
	if not employee_instance:
		return False
	else:
		return True
	
def employee_report_generation(empID,startDate,endDate,reportType):
	start = startDate.strftime("%Y-%m-%d")
	end = endDate.strftime("%Y-%m-%d")
	filterargs = { 'empID': empID, 'startDate': xrange(start, end), 'endDate': xrange(start, end) }
	if reportType == 'LEAVE BALANCES':
		rep = EmployeeLeaveMaster.objects.filter(empID=empID).values()
		report = [entry for entry in rep]  
		return report
	if reportType == 'HISTORY':
		rep = EmployeeLeaveTransaction.objects.filter(**filterargs).values()
		se1 = se.objects.filter(empID=empID)
		report = [entry for entry in se]
		return report


	
 		
	 
	
	
	
	
	
	
	
	
	
	
	
	
	
	

