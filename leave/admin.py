from django.contrib import admin
from django.contrib import admin

from .models import *

admin.site.register(Employee)
admin.site.register(EmployeeLeaveMaster)
admin.site.register(EmployeeLeaveTransaction)
admin.site.register(EmployeeAddress)
admin.site.register(EmployeeProject)
admin.site.register(PhoneNumber)
admin.site.register(Project)
admin.site.register(EmployeeLeaveLog)
admin.site.register(Leave)
admin.site.register(IsEmployeeHR)
admin.site.register(Logincredentials)

try:
    from admin_import.options import add_import
except ImportError:
    pass
else:
    add_import(InviteeAdmin)


