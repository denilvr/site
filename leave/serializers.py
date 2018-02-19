from rest_framework import serializers
from models import *
from django.core.urlresolvers import reverse

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
		model = Employee
		field = ('empID','phoneNumber')
		
class EmployeeTransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmployeeLeaveTransaction
		field = ('startDate','endDate','duration','leave','empID')
		
class EmployeeLeaveMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmployeeLeaveMaster
		field = ('empID','clLeft','slLeft','vlLeft','elLeft')
