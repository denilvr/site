from django.conf.urls import include, url
from . import views
from leave.views import *


urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^leaveApplication/$',views.leave_application,name='leaveApplication'),
    #url(r'^register/$',views.create_user, name='register'),
    url(r'^checkavailable/$',views.checkavailable, name='checkavailable'),
    #url(r'^login/$',views.login_user, name='login'),
    url(r'^findPerson/$', views.find_person,name='findPerson'),
    url(r'^cancelLeave/$', views.cancel_leave,name='cancelLeave'),
    url(r'^leaveBalanceReport/$', views.leave_balance_report,name='leaveBalanceReport'),
    url(r'^leaveHistoryReport/$', views.leave_history_report,name='leaveHistoryReport'),
    #url(r'^leaveHistoryReport/method="POST"?$', views.leave_history_report2,name='leaveHistoryReport2'),
    url(r'^add_employee/$', views.add_employee,name='add_employee'),
    url(r'^adjust_leaves/$', views.adjust_leaves,name='adjust_leaves'),
    url(r'^update_holidays/$', views.update_holidays,name='update_holidays'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    #url(r'^accounts/signup/$', views.signup, name='signup'),leave/leaveHistoryReport/method="POST"?
    

]
