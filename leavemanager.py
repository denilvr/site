import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

#Global Variables
#import calendar
#print calendar.__file__

###########################################################################################################

import requests
import json
import re

headers={"content_type":"application/json"}

    
############################################################################################################

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        try:
            url="http://127.0.0.1:8000/leave/checkavailable/"
            data={"incoming":"hi"}
            r=requests.post(url,data=json.dumps(data),headers=headers)
            request_response=r.content
            status=re.findall(r'(?<="status":\s")(.*?)(?=")',request_response)
            status=str(status[0])
        except:
            status='Fail'


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        
        self.frames = {}
        for F in (Homepage, Apply_for_leave, Cancel_leave, Leave_balance, Leave_History, login, register, FirstPage, intermediate_true, intermediate_false, registration_success, registration_failed, leavehistoryAck, leavehistoryNAck, leave_balance_details,Cancel_leave_success,Cancel_leave_failed, Employee_not_found, Leave_App_True, other_apply_errors, Server_not_available):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        if status=='Success':
            self.show_frame("FirstPage")
        else:
            self.show_frame("Server_not_available")
       


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def multifunction(self):
        if label1_1.winfo_exists()==1:
            label1_1.destroy()
            label1_2.destroy()
            label1_3.destroy()
            label1_4.destroy()
            label2_1.destroy()
            label2_2.destroy()
            label2_3.destroy()
            label2_4.destroy()

            self.show_frame("Homepage")

        else:
            self.show_frame("Homepage")




    #All check(with server online)
    def loginuser(self, username, password):
        url="http://127.0.0.1:8000/leave/login/"
        data={"username":str(username), "password":str(password)}
        r=requests.post(url,data=json.dumps(data),headers=headers)
        request_response=r.content
        print(request_response)
        access_statement=re.findall(r'(?<="message":\s")(.*?)(?=",)',request_response)
        access_statement=str(access_statement[0])
        print(access_statement)
        global identity_login
        identity_login=re.findall(r'(?<="ID":\s")(.*?)(?="})',request_response)
        identity_login=str(identity_login[0])
        print(identity_login)
        global nextpage
        if access_statement=='True':
            nextpage='Homepage'#'intermediate_true'
        else:
            nextpage='intermediate_false'

        self.show_frame(nextpage)
        
    # All check(with server online)
    def registeruser(self, empID, username, password):
        print (empID)
        print (username)
        print (password)
        if len(employeeID_register.get())==0 or len(username_register.get())==0 or len(password_register.get())==0 :
            self.show_frame('register')
        else:
            url="http://127.0.0.1:8000/leave/register/"
            data={"emplID":str(empID), "username":str(username), "password":str(password)}
            r=requests.post(url,data=json.dumps(data),headers=headers)
            request_response=r.content
            status=re.findall(r'(?<="status":\s")(.*?)(?=")',request_response)
            status=str(status[0])
            identity_register=re.findall(r'(?<="ID":\s")(.*?)(?="})',request_response)
            identity_register=str(identity_register[0])
            
            if status=='Success':
                nextpage='registration_success'
            else:
                nextpage='registration_failed'

            self.show_frame(nextpage)

    # All check(with server online)      
    def leaveHistory(self,useruniqueID, startDate, endDate):
        print(useruniqueID)
        print(startDate)
        print(endDate)
        url="http://127.0.0.1:8000/leave/leaveHistoryReport/"
        data={"employee_id":"None","user unique_id": str(useruniqueID),"start date":str(startDate),"end date":str(endDate),"name":"None"}
        r=requests.post(url,data=json.dumps(data),headers=headers)
        request_response=r.content
        status=re.findall(r'(?<=message":\s")(.*?)(?=")',request_response)
        print(status)
        status=str(status[0])
        print(status)

        if status=='Success':
            nextpage='leavehistoryAck'
        else:
            nextpage='leavehistoryNAck'

        self.show_frame(nextpage)

    def leaveBalance(self,empID):
        url="http://127.0.0.1:8000/leave/leaveBalanceReport/"
        data={"employee_id":"None", "user unique_id":str(empID), "name":"None"}
        r=requests.post(url,data=json.dumps(data),headers=headers)
        request_response=r.content
        casual_1=re.findall(r"(?<='casualLeavesLeft':\s)(.*?)(?=,)",str(request_response))
        casual=str(casual_1[0])
        print(casual)
        sick_1=re.findall(r"(?<='sickLeavesLeft':\s)(.*?)(?=,)",str(request_response))
        sick=str(sick_1[0])
        print(sick)
        vacation_1=re.findall(r"(?<='VacationLeavesLeft':\s)(.*?)(?=,)",str(request_response))
        vacation=str(vacation_1[0])
        print(vacation)
        earn_1=re.findall(r"(?<='earnLeavesLeft':\s)(.*?)(?=})",str(request_response))
        earn=str(earn_1[0])
        print(earn)

        global label1_1
        label1_1 = tk.Label(self, text="Casual Leaves Left: ", font=("arial",15,"bold"),fg='steelblue')
        label1_1.place(x=100, y=200)

        global label1_2
        label1_2 = tk.Label(self, text="Sick Leaves Left: ", font=("arial",15,"bold"),fg='steelblue')
        label1_2.place(x=100, y=240)

        global label1_3
        label1_3 = tk.Label(self, text="Vacation Leaves Left: ", font=("arial",15,"bold"),fg='steelblue')
        label1_3.place(x=100, y=280)

        global label1_4
        label1_4 = tk.Label(self, text="Earn Leaves Left: ", font=("arial",15,"bold"),fg='steelblue')
        label1_4.place(x=100, y=320)

        global label2_1
        label2_1 = tk.Label(self, text=casual, font=("arial",15,"bold"),fg='steelblue')
        label2_1.place(x=350, y=200)

        global label2_2
        label2_2 = tk.Label(self, text=sick, font=("arial",15,"bold"),fg='steelblue')
        label2_2.place(x=350, y=240)

        global label2_3
        label2_3 = tk.Label(self, text=vacation, font=("arial",15,"bold"),fg='steelblue')
        label2_3.place(x=350, y=280)

        global label2_4
        label2_4 = tk.Label(self, text=earn, font=("arial",15,"bold"),fg='steelblue')
        label2_4.place(x=350, y=320)

 
     


    # All check(with server online)     
    def cancelLeave(self,InEndDate, CurEndDate, useruniqueID, leavetype, empID):
        print(InEndDate)
        print(CurEndDate)
        print(useruniqueID)
        print(leavetype)
        print(empID)
        url="http://127.0.0.1:8000/leave/cancelLeave/"  
        data={"employee_id":str(empID), "current end date":str(CurEndDate) , "initial end date": str(InEndDate) , "user unique_id": str(useruniqueID),"leave type": str(leavetype)}
        r=requests.post(url,data=json.dumps(data),headers=headers)
        request_response=r.content
        status=re.findall(r'(?<="status":\s")(.*?)(?=",)',str(request_response))
        status=str(status[0])
        

        if status=='Success':
            self.show_frame('Cancel_leave_success')
        else:
            self.show_frame('Cancel_leave_failed')

    
    # All check(with server online) 
    def applyforleave(self,startDate, endDate, leavetype, empID, useruniqueID):
        print(startDate)
        print(endDate)
        print(leavetype)
        print(empID)
        print(useruniqueID)
        url="http://127.0.0.1:8000/leave/leaveApplication/"
        data={'start date': str(startDate),"end date":str(endDate),"employee_id": str(empID),"leave type": str(leavetype),"user unique_id":str(useruniqueID)}
        r=requests.post(url,data=json.dumps(data),headers=headers)
        request_response=r.content
        status=re.findall(r'(?<=message":\s")(.*?)(?=")',str(request_response))
        status=str(status[0])
        print(status)
        if status=='your leave request has been accepted':
            self.show_frame('Leave_App_True')
        elif status=='Employee not found':
            self.show_frame('Employee_not_found')
        else:
            self.show_frame('other_apply_errors')

############################################################################################################################


class Homepage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #photo = tk.PhotoImage(file='cse.png') 
        label = tk.Label(self, text="Leave Manager Console", font=("arial",40,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)


        button1 = tk.Button(self, text="Leave Application",height=3, width=25, bg='lightgreen',command=lambda: controller.show_frame("Apply_for_leave"))
        button2 = tk.Button(self, text="Cancel Leave",height=3, width=25, bg='lightgreen',command=lambda: controller.show_frame("Cancel_leave"))
        button3 = tk.Button(self, text="Leave Balance",height=3, width=25, bg='lightgreen',command=lambda: controller.show_frame("Leave_balance"))
        button4 = tk.Button(self, text="Leave History",height=3, width=25, bg='lightgreen',command=lambda: controller.show_frame("Leave_History"))
        button5 = tk.Button(self, text="LogOut",height=3, width=25, bg='lightgreen',command=lambda: controller.show_frame("FirstPage"))
        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        button5.pack()

        sometext=""
        label = tk.Label(self, text=sometext, font=("arial",10,"bold"),fg='steelblue')
        label.pack(side=tk.LEFT, fill="x", pady=10)


class Apply_for_leave(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Apply for leave", font=("arial",40,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

        StartLabel= tk.Label(self,text='Start Date',font=("arial",15,"bold"),fg='black')
        StartLabel.place(x=100, y=100)
        startlabel=tk.StringVar()
        startlabel_Entry_box= tk.Entry(self, textvariable=startlabel, bg='lightgreen')
        startlabel_Entry_box.place(x=380, y=110)

        EndLabel= tk.Label(self,text='End Date',font=("arial",15,"bold"),fg='black')
        EndLabel.place(x=100, y=140)
        endlabel=tk.StringVar()
        endlabel_Entry_box= tk.Entry(self, textvariable=endlabel, bg='lightgreen')
        endlabel_Entry_box.place(x=380, y=150)


        LeaveTypeLabel= tk.Label(self,text='Leave type',font=("arial",15,"bold"),fg='black')
        LeaveTypeLabel.place(x=100, y=180)
        leavetypelabel=tk.StringVar()
        leavetype_Entry_box= tk.Entry(self, textvariable=leavetypelabel, bg='lightgreen')
        leavetype_Entry_box.place(x=380, y=190)

        button1 = tk.Button(self, text="Submit Details", height=3, width=20, bg='blue',command=lambda: controller.applyforleave(startlabel.get(),endlabel.get(),leavetypelabel.get(),identity_login,identity_login))
        button1.place(x=250, y=250)

        button2 = tk.Button(self, text="Go to the Home page", height=2, width=15, bg='gray',command=lambda: controller.show_frame("Homepage"))
        button2.pack(side=tk.RIGHT, fill="x", pady=10)


class Cancel_leave(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Cancel Leave", font=("arial",40,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

        StartLabel= tk.Label(self,text='Initial End date',font=("arial",15,"bold"),fg='black')
        StartLabel.place(x=100, y=100)
        initialendDate=tk.StringVar()
        startlabel_Entry_box= tk.Entry(self, textvariable=initialendDate, bg='lightgreen')
        startlabel_Entry_box.place(x=380, y=110)

        EndLabel= tk.Label(self,text='New End Date',font=("arial",15,"bold"),fg='black')
        EndLabel.place(x=100, y=140)
        newendDate=tk.StringVar()
        endlabel_Entry_box= tk.Entry(self, textvariable=newendDate, bg='lightgreen')
        endlabel_Entry_box.place(x=380, y=150)


        LeaveTypeLabel= tk.Label(self,text='Leave type you applied for',font=("arial",15,"bold"),fg='black')
        LeaveTypeLabel.place(x=100, y=180)
        leavetypelabel=tk.StringVar()
        leavetype_Entry_box= tk.Entry(self, textvariable=leavetypelabel, bg='lightgreen')
        leavetype_Entry_box.place(x=380, y=190) 


        button1 = tk.Button(self, text="Submit Details", height=3, width=20, bg='blue',command=lambda: controller.cancelLeave(initialendDate.get(),newendDate.get(),identity_login,leavetypelabel.get(),identity_login))
        button1.place(x=250, y=250)

        button2 = tk.Button(self, text="Go to Home page",height=2, bg='gray',command=lambda: controller.show_frame("Homepage"))
        button2.pack(side=tk.RIGHT, fill="x", pady=10)


class Leave_balance(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Check your leave balance", font=("arial",40,"bold"),fg='steelblue') 
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Click here to check leave balance",height=5, width=35 ,bg='aqua',command=lambda: controller.leaveBalance(identity_login))
        button1.pack()

        button2= tk.Button(self, text="Back to Home page",height=2, width=15, bg='gray',command=lambda: controller.multifunction())
        button2.pack(side=tk.RIGHT, fill="x", pady=10)

class Leave_History(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Request for leave history", font=("arial",40,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

        StartLabel= tk.Label(self,text='Start Date',font=("arial",15,"bold"),fg='black')
        StartLabel.place(x=100, y=100)
        startDate=tk.StringVar()
        startlabel_Entry_box= tk.Entry(self, textvariable=startDate, bg='lightgreen')
        startlabel_Entry_box.place(x=380, y=110)

        EndLabel= tk.Label(self,text='End Date',font=("arial",15,"bold"),fg='black')
        EndLabel.place(x=100, y=140)
        endDate=tk.StringVar()
        endlabel_Entry_box= tk.Entry(self, textvariable=endDate, bg='lightgreen')
        endlabel_Entry_box.place(x=380, y=150)



        button1 = tk.Button(self, text="Submit Details", height=3, width=20, bg='blue',command=lambda: controller.leaveHistory(identity_login,startDate.get(),endDate.get()))
        button1.place(x=250, y=250)
        button2= tk.Button(self, text="Back to Home page",height=2, width=15, bg='gray',command=lambda: controller.show_frame("Homepage"))
        button2.pack(side=tk.RIGHT, fill="x", pady=10)


class FirstPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='LightSlateGray')
        self.controller = controller
        #photo = tk.PhotoImage(file='cse.png') 
        label = tk.Label(self, text="Leave Manager", font=("arial",40,"bold"),fg='black',bg='LightSlateGray')
        label.pack(side="top", fill="x", pady=10)


        button1 = tk.Button(self, text="Login",height=3, width=25, bg='Pink',command=lambda: controller.show_frame("login"))
        button2 = tk.Button(self, text="Register",height=3, width=25, bg='Pink',command=lambda: controller.show_frame("register"))
        
        button1.bind('<Return>',controller.show_frame("login"))

        button1.pack()
        button2.pack()

        label = tk.Label(self, text="@CSE_Club_IIST", font=("arial",10,"bold"),fg='black',bg='LightSlateGray')
        label.pack(side=tk.LEFT, fill="x", pady=10)




        

class login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Login", font=("arial",40,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

        StartLabel= tk.Label(self,text='username',font=("arial",15,"bold"),fg='black')
        StartLabel.place(x=100, y=100)
        global username_login
        username_login=tk.StringVar()
        #username_login=username_login.get()
        startlabel_Entry_box= tk.Entry(self, textvariable=username_login, bg='lightgreen')
        startlabel_Entry_box.place(x=380, y=110)

        EndLabel= tk.Label(self,text='password',font=("arial",15,"bold"),fg='black')
        EndLabel.place(x=100, y=140)
        global password_login
        password_login=tk.StringVar()
        #password_login=password_login.get()
        endlabel_Entry_box= tk.Entry(self, textvariable=password_login, bg='lightgreen',show="*")
        endlabel_Entry_box.place(x=380, y=150)

        

        button1 = tk.Button(self, text="Submit", height=3, width=20, bg='blue',command=lambda: controller.loginuser(username_login.get(),password_login.get()))
        button1.place(x=250, y=200)
        #button1.bind('<Return>',command=lambda: controller.loginuser(username_login.get(),password_login.get()))
        button2= tk.Button(self, text="Back to Home page",height=2, width=15, bg='gray',command=lambda: controller.show_frame("FirstPage"))
        button2.pack(side=tk.RIGHT, fill="x", pady=10)

        



class register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Register", font=("arial",40,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

        StartLabel= tk.Label(self,text='Your Employee ID',font=("arial",15,"bold"),fg='black')
        StartLabel.place(x=100, y=100)
        global employeeID_register
        employeeID_register=tk.StringVar()
        startlabel_Entry_box= tk.Entry(self, textvariable=employeeID_register, bg='lightgreen')
        startlabel_Entry_box.place(x=380, y=110)

        EndLabel= tk.Label(self,text='Enter Username',font=("arial",15,"bold"),fg='black')
        EndLabel.place(x=100, y=140)
        global username_register
        username_register=tk.StringVar()
        endlabel_Entry_box= tk.Entry(self, textvariable=username_register, bg='lightgreen')
        endlabel_Entry_box.place(x=380, y=150)

        LeaveTypeLabel= tk.Label(self,text='Enter Password',font=("arial",15,"bold"),fg='black')
        LeaveTypeLabel.place(x=100, y=180)
        global password_register
        password_register=tk.StringVar()
        leavetype_Entry_box= tk.Entry(self, textvariable=password_register, bg='lightgreen',show="*")
        leavetype_Entry_box.place(x=380, y=190)

        
        button1 = tk.Button(self, text="Register",height=5, width=15 ,bg='aqua',command=lambda:controller.registeruser(employeeID_register.get(),username_register.get(),password_register.get()) )
        button1.place(x=250, y=250)

        button2= tk.Button(self, text="Back to Home page",height=2, width=15, bg='gray',command=lambda: controller.show_frame("FirstPage"))
        button2.pack(side=tk.RIGHT, fill="x", pady=10)

#####################################################################################################################

class intermediate_true(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Verifying Credentails", font=("arial",40,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)


        StartLabel= tk.Label(self,text='Correct Credentials',font=("arial",15,"bold"),fg='black')
        StartLabel.place(x=100, y=250)

        button1 = tk.Button(self, text="Move to console",height=5, width=15 ,bg='aqua',command=lambda: controller.show_frame("Homepage"))
        button1.place(x=250, y=300)


class intermediate_false(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Verifying Credentails", font=("arial",40,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

       
        StartLabel= tk.Label(self,text='Incorrect Credentials',font=("arial",15,"bold"),fg='black')
        StartLabel.place(x=100, y=250)

        button1 = tk.Button(self, text="Back",height=5, width=15 ,bg='aqua',command=lambda: controller.show_frame("login"))
        button1.place(x=250, y=300)

#####################################################################################################################3

class registration_success(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="You are successfully registered", font=("arial",20,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)


        button1 = tk.Button(self, text="Login",height=5, width=15 ,bg='aqua',command=lambda: controller.show_frame("login"))
        button1.place(x=250, y=300)


class registration_failed(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Something went wrong.Please register Again", font=("arial",30,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)


        button1 = tk.Button(self, text="Login",height=5, width=15 ,bg='aqua',command=lambda: controller.show_frame("register"))
        button1.place(x=250, y=300)

#####################################################################################################################

class leavehistoryNAck(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Something went wrong.Please try Again", font=("arial",10,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go back",height=5, width=15 ,bg='aqua',command=lambda: controller.show_frame("Homepage"))
        button1.place(x=250, y=300)


class leavehistoryAck(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Leave History Report has been mailed to your email address", font=("arial",10,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go back",height=5, width=15 ,bg='aqua',command=lambda: controller.show_frame("Homepage"))
        button1.place(x=250, y=300)

######################################################################################################################
class leave_balance_details(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        

        label1 = tk.Label(self, text="List of leaves left", font=("arial",20,"bold"),fg='steelblue')
        label1.pack(side="top", fill="x", pady=10)

        label1_1 = tk.Label(self, text="Casual Leaves Left: ", font=("arial",15,"bold"),fg='steelblue')
        label1_1.place(x=100, y=100)

        label1_2 = tk.Label(self, text="Sick Leaves Left: ", font=("arial",15,"bold"),fg='steelblue')
        label1_2.place(x=100, y=140)

        label1_3 = tk.Label(self, text="Vacation Leaves Left: ", font=("arial",15,"bold"),fg='steelblue')
        label1_3.place(x=100, y=180)

        label1_4 = tk.Label(self, text="Earn Leaves Left: ", font=("arial",15,"bold"),fg='steelblue')
        label1_4.place(x=100, y=220)

        label2_1 = tk.Label(self, text="", font=("arial",15,"bold"),fg='steelblue')
        label2_1.place(x=350, y=100)

        label2_2 = tk.Label(self, text="", font=("arial",15,"bold"),fg='steelblue')
        label2_2.place(x=350, y=140)

        label2_3 = tk.Label(self, text="", font=("arial",15,"bold"),fg='steelblue')
        label2_3.place(x=350, y=180)

        label2_4 = tk.Label(self, text="", font=("arial",15,"bold"),fg='steelblue')
        label2_4.place(x=350, y=220)

        button1 = tk.Button(self, text="Go back",height=5, width=15 ,bg='aqua',command=lambda: controller.show_frame("Homepage"))
        button1.pack(side=tk.RIGHT)

###########################################################################################################################


class Cancel_leave_success(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Your leave(s) has been successfully cancelled", font=("arial",10,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go back",height=5, width=15 ,bg='aqua',command=lambda: controller.show_frame("Homepage"))
        button1.place(x=250, y=300)    

class Cancel_leave_failed(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Something went wrong. Please try again", font=("arial",10,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go back",height=5, width=15 ,bg='aqua',command=lambda: controller.show_frame("Homepage"))
        button1.place(x=250, y=300)    

###################################################################################################


class Leave_App_True(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Your leave has been accepted", font=("arial",10,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go back",height=5, width=15 ,bg='aqua',command=lambda: controller.show_frame("Homepage"))
        button1.place(x=250, y=300)   

class Employee_not_found(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Your details are unavailable in the database", font=("arial",10,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go back",height=5, width=15 ,bg='aqua',command=lambda: controller.show_frame("Homepage"))
        button1.place(x=250, y=300)

class other_apply_errors(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Something went wrong. Please try again", font=("arial",10,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go back",height=5, width=15 ,bg='aqua',command=lambda: controller.show_frame("Homepage"))
        button1.place(x=250, y=300)

############################################################################################################################


class Server_not_available(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Server not available", font=("arial",40,"bold"),fg='steelblue')
        label.pack(side="top", fill="x", pady=10)


if __name__ == "__main__":
    app = SampleApp()
    app.title("Leave Manager Application")
    app.geometry("640x400+0+0")

    
    app.mainloop()
