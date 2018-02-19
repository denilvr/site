from .models import CustomModel, Employee
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from django.forms.util import ErrorList
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
#x = None

ARR = [0,0]

def validate_startDate(value):
	ARR[0] = value
	if value < timezone.now():
		raise ValidationError(
            _('Please enter a future date'),
            params={'value': value},
        )
def validate_endDate(value):
	
	
	print(ARR[1])
	#x = func()
	if value < ARR[0]:
		raise ValidationError(
            _('Please enter a date after the start date'),
            params={'value': value},
        )

LEAVE_CHOICES = (
			   ('CASUAL LEAVE','CASUAL LEAVE') ,
			   ('SICK LEAVE','SICK LEAVE' ),
			   ('VACATION LEAVE','VACATION LEAVE') ,
			   ('EARN LEAVE','EARN LEAVE' ),
			   ('MATERNITY LEAVE','MATERNITY LEAVE'),
			   ('WORK FROM HOME','WORK FROM HOME'),
			)

class LeaveApplicationForm(forms.Form):
	leave = forms.ChoiceField(choices=LEAVE_CHOICES,label='Leave ')
	startDate=forms.DateTimeField(label='Start Date ',validators=[validate_startDate])
	endDate=forms.DateTimeField(label='End Date ',validators=[validate_endDate])


class SignUpForm(UserCreationForm):
	empID = forms.CharField(max_length=10, required=True, help_text='Required')
	first_name = forms.CharField(max_length=30, required=True, help_text='Required')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
	email = forms.EmailField(max_length=254, help_text='Enter a valid email address.')

	class Meta:
		model = User
		fields = ('empID','username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
		#fields = ('username','password1')
	

# class EmployeeForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         fields = ('empID',)

class DateInput(forms.DateInput):
	input_type = 'date'


class CustomModelForm(forms.ModelForm):

	class Meta:
		model = CustomModel
		fields = ('leave','startDate','endDate')
		widgets = {
			'startDate': DateInput(),
			'endDate': DateInput()
			
		}
		labels = {
			'startDate': ('Start Date '),
			'endDate': ('End Date '),
			'leave': ('Leave '),
		}
	
