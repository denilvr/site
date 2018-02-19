from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class Department(models.Model):
	deptID=models.CharField(max_length=10,null=False,unique=True,primary_key=True)
	deptName = models.CharField(max_length=100)
	dateCreated = models.DateField('date created',null = True)
	dateUpdated = models.DateField('date updated',null = True)
	def __unicode__(self):
		return str(self.deptName)

#Model for employees
class Logincredentials(models.Model):
	EmpID=models.CharField(max_length=10)
	username=models.CharField(max_length=32)
	password=models.CharField(max_length=256)
	def __unicode__(self):
		return str(self.username)



class Employee(models.Model):
	
	author = models.ForeignKey('auth.User',null=True,on_delete=models.CASCADE)
	empID = models.CharField(max_length=10,null=False,unique=True,primary_key=True)
	#empID = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	empUniqueID=models.CharField(max_length = 10, null=True,blank=True,default=None)
	firstName = models.CharField(max_length=100)
	lastName= models.CharField(max_length=100)	
	email = models.EmailField(null=True)
	joiningDate= models.DateField('date published',null = True)
	designation = models.CharField(max_length = 50,blank=True)
	address = models.OneToOneField('EmployeeAddress',null =True,blank=True,on_delete=models.CASCADE)
	phoneNumber = models.OneToOneField('PhoneNumber',null = True,blank=True,on_delete=models.CASCADE,)	
	dateCreated = models.DateField('date created',null = True,blank=True)
	dateUpdated = models.DateField('date updated',null = True,blank=True)
	manager = models.CharField(max_length = 40)
	managerID = models.CharField(max_length = 10)
	is_hr=models.BooleanField(default=False)
	gender = models.CharField(null = True,max_length=20)
	#projectID=models.ForeignKey('Project')
	def __unicode__(self):
		return str(self.empID)



class IsEmployeeHR(models.Model):
	empID = models.OneToOneField('Employee',on_delete=models.CASCADE)
	is_hr = models.IntegerField(null=True)


class PhoneNumber(models.Model):
	
	phoneID= models.IntegerField(null=False,unique=True,primary_key=True)
	empID=models.OneToOneField('Employee',on_delete=models.CASCADE,)
	phoneType = models.CharField(max_length=20)	
	phoneNumber=models.IntegerField(null=True)
	dateCreated = models.DateField('date created',null = True)
	dateUpdated = models.DateField('date updated',null = True)	
	def __unicode__(self):
		return  str(self.phoneNumber)


class Leave(models.Model):
	leaveID=models.CharField(max_length=10,null=False,unique=True,primary_key=True)
	leaveName = models.CharField(max_length = 30)
	totalSanctioned = models.IntegerField()
	dateCreated = models.DateField('date created',null = True)
	dateUpdated = models.DateField('date updated',null = True)
	def __unicode__(self):
		return str(self.leaveName)	


class Project(models.Model):
	projectID=models.CharField(max_length=10,null=False,unique=True,primary_key=True)
	#deptID=models.OneToOneField('Department')
	projectName= models.CharField(max_length=30,null=True,default=None)
	startDate = models.DateField('date published',null = True)
	endDate = models.DateField('date published',null = True)
	dateCreated = models.DateField('date created',null = True)
	dateUpdated = models.DateField('date updated',null = True)
	def __unicode__(self):
		return str(self.projectName)


class EmployeeProject(models.Model):
	id=models.AutoField(primary_key=True)
	empID=models.ForeignKey('Employee',on_delete=models.CASCADE)
	projectID=models.ForeignKey('Project',on_delete=models.CASCADE)
	dateCreated = models.DateField('date created',null = True)
	dateUpdated = models.DateField('date updated',null = True)
	def __unicode__(self):
		return str(self.empID)

class EmployeeAddress(models.Model):	
	empID = models.OneToOneField('Employee',on_delete=models.CASCADE)
	permanentAddress = models.CharField(max_length=300)
	presentAddress = models.CharField(max_length = 300)
	dateCreated = models.DateField('date created',null = True)
	dateUpdated = models.DateField('date updated',null = True)
	def __unicode__(self):
		return str(self.empID)

class EmployeeLeaveMaster(models.Model):
	empID=models.OneToOneField('Employee',primary_key=True,on_delete=models.CASCADE)
	#work_from_home_availed = models.FloatField(default=0)
	casualLeavesLeft = models.FloatField(default =0)
	
	sickLeavesLeft = models.FloatField(default =0)
	
	VacationLeavesLeft = models.FloatField(default =0)

	#vacationLeavesLeft = models.FloatField(default =0)
	
	earnLeavesLeft = models.FloatField(default =0)
	
	#maternityLeavesLeft = models.IntegerField(default =0)
	
	financialYear = models.CharField(max_length = 10)	
	dateCreated = models.DateField('date created',null = True)
	dateUpdated = models.DateField('date updated',null = True)
	def __unicode__(self):
		emp = str(self.empID)
		return emp

class EmployeeLeaveLog(models.Model):
	id=models.AutoField(primary_key=True)
	date = models.DateTimeField('leave date')
	empID = models.ForeignKey('Employee',on_delete=models.CASCADE)	
	leaveType = models.CharField(max_length = 20)
	#leaveDuration  = models.CharField(max_length = 10)
	#ApplicationSubmitted=models.BooleanField(default=False)
	dateCreated = models.DateField('date created',null = True)
	dateUpdated = models.DateField('date updated',null = True)
	def __unicode__(self):
		emp = str(self.empID)
		return emp
	
class EmployeeLeaveTransaction(models.Model):
	#phoneID=models.CharField(max_length=10)
	# = models.CharField(max_length=10,primary_key=True)
	empID=models.ForeignKey('Employee',on_delete=models.CASCADE)
	leave = models.CharField(max_length=30,default = '')
	startDate=models.DateTimeField('date published',null=True)
	endDate=models.DateTimeField('date published')
	duration = models.FloatField(default=0)
	status= models.BooleanField(default=0)
	messageReceived=models.TextField(max_length=100,null = True)


	def __unicode__(self):
		emp = str(self.empID)
		return emp
LEAVE_CHOICES = (
			   ('CASUAL LEAVE','CASUAL LEAVE') ,
			   ('SICK LEAVE','SICK LEAVE' ),
			   ('VACATION LEAVE','VACATION LEAVE') ,
			   ('EARN LEAVE','EARN LEAVE' ),
			   ('MATERNITY LEAVE','MATERNITY LEAVE'),
			   ('WORK FROM HOME','WORK FROM HOME'),
			)

class CustomModel(models.Model):
	#requestID=models.CharField(max_length=10)
	# = models.CharField(max_length=10,primary_key=True)
	empID = models.CharField(max_length=10,null=False,unique=True,primary_key=True)
	leave = models.CharField(max_length=30,choices=LEAVE_CHOICES,default = '')
	startDate=models.DateTimeField(null=True)
	endDate=models.DateTimeField(null=True)
	#duration = models.FloatField(default=0)
	#status= models.BooleanField(default=0)
	#message=models.TextField(max_length=100,null = True)



