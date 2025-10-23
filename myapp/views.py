import random
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from e_votting import settings
from myapp.models import *



def logout_get(request):
    logout(request)
    return redirect('/myapp/login_get/')


def login_get(request):
    # return render(request,'login.html')
    return render(request,'login_index.html')


def login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(request,username=username,password=password)

    print(user,"====")
    if user is not None:
        print(1)

        if user.groups.filter(name='Subadmin').exists():
            print("ooooooooooooooooooooooo")
            login(request, user)
            return redirect('/myapp/homesub_s/')
        elif user.groups.filter(name='Admin').exists():
            print(2)
            login(request, user)
            return redirect('/myapp/adminhome/')
        elif user.groups.filter(name='Electioncoordinator').exists():
            print(3)
            login(request, user)
            return redirect('/myapp/coordinator_home/')
        else:
            print(4)
            messages.error(request,"invalid user name or password")
            return redirect('/myapp/login_get/')
            # return redirect('/myapp/adminhome/')

    else:
        print(5)
        messages.error(request,"user not found")
        return redirect('/myapp/login_get/')

def forgot_password(request):
    return render(request, 'forgotten_password.html')

def forgotpassword_post(request):

    email = request.POST['email']

    if User.objects.filter(username=email).exists():

        import random
        new_pass = random.randint(00000, 99999)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("trainingstarted@gmail.com", " nlxasujxgazlbmgz")  # App Password
        to = email
        subject = "Test Email"
        body = "Your new password is " + str(new_pass)
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail("s@gmail.com", to, msg)  # Disconnect from the server
        server.quit()

        user = User.objects.get(username=email)
        user.set_password(str(new_pass))
        user.save()

        return redirect('/myapp/login_get/')
    else:
        messages.warning(request, 'email not  exists')
        return redirect('/myapp/forgot_password/')


############ ADMIN #########

@login_required(login_url='/myapp/login_get/')
def adminhome(request):
    return render(request,"admin/adminindex.html")

@login_required(login_url='/myapp/login_get/')  
def admin_addcourse(request):
    res = Department.objects.all()
    return render(request,'admin/add course.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def admin_addcourse_post(request):
    course=request.POST['course']
    department= request.POST['department']
    cobj=Course()
    cobj.coursename=course
    cobj.DEPARTMENT_id=department
    cobj.save()
    messages.success(request,"Added Successfull")
    return redirect('/myapp/admin_viewcourse/#abc')


@login_required(login_url='/myapp/login_get/')  
def admin_editcourse(request,id):
    res = Department.objects.all()
    data=Course.objects.get(id=id)
    return render(request,'admin/edit course.html',{'data':data,'dept':res})

@login_required(login_url='/myapp/login_get/')  
def admin_editcourse_post(request):
    department=request.POST['department']
    course=request.POST['course']
    id=request.POST['id']
    cobj = Course.objects.get(id=id)
    cobj.coursename = course
    cobj.DEPARTMENT_id = department
    cobj.save()
    messages.success(request, "Added Successfull")
    return redirect('/myapp/admin_viewcourse/#abc')

@login_required(login_url='/myapp/login_get/')  
def delete_course(request,cid):
    Course.objects.filter(id=cid).delete()
    messages.success(request,"Delete Successfull")
    return redirect('/myapp/admin_viewcourse/#abc')

@login_required(login_url='/myapp/login_get/')  
def admin_viewcourse(request):
    res = Course.objects.all()
    return render(request,'admin/view course.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def admin_adddepartment(request):
    return render(request,'admin/add department.html')

@login_required(login_url='/myapp/login_get/')  
def admin_adddepartment_post(request):
    department=request.POST['department']
    dobj=Department()
    dobj.department=department
    dobj.save()
    messages.success(request,"Added Successfull")
    return redirect('/myapp/admin_viewdepartment/#abc')

@login_required(login_url='/myapp/login_get/')  
def admin_editdepartment(request,id):
    data = Department.objects.get(id=id)
    return render(request,'admin/edit department.html',{'data':data})

@login_required(login_url='/myapp/login_get/')  
def admin_editdepartment_post(request):
    department=request.POST['department']
    id=request.POST['id']
    dobj = Department.objects.get(id=id)
    dobj.department = department
    dobj.save()
    messages.success(request, "Edited Successfull")
    return redirect('/myapp/admin_viewdepartment/#abc')

@login_required(login_url='/myapp/login_get/')  
def delete_department(request,id):
    Department.objects.filter(id=id).delete()
    messages.success(request,"Delete Successfull")
    return redirect('/myapp/admin_viewdepartment/#abc')

@login_required(login_url='/myapp/login_get/')  
def admin_viewdepartment(request):
    res=Department.objects.all()
    return render(request,'admin/view department.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def admin_changepassword(request):
    return render(request,'admin/Change password.html')

@login_required(login_url='/myapp/login_get/')  
def admin_changepassword_post(request):
    enteroldpassword=request.POST['enter old password']
    enternewpassword=request.POST['enter new password']
    confirmpassword=request.POST['confirm password']
    user=request.user
    if user.check_password(enteroldpassword):
        if enternewpassword==confirmpassword:
            user.set_password(enternewpassword)
            user.save()
            return redirect('/myapp/login_get/')
        else:
            return redirect('/myapp/admin_changepassword/#abc')
    else:
        return redirect('/myapp/admin_changepassword/#abc')

@login_required(login_url='/myapp/login_get/')  
def admin_Addsubadmin(request):
    res = Department.objects.all()
    return render(request,'admin/Add sub admin.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def admin_Addsubadmin_post(request):
    name=request.POST['name']
    DOB=request.POST['DOB']
    gender=request.POST['gender']
    email=request.POST['email']
    Phonenumber=request.POST['phonenumber']
    department=request.POST['department']
    photo=request.FILES['photo']
    # import random
    # password=random.randint(0000,9999)

    fs=FileSystemStorage()
    date=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    fs.save(date,photo)
    path=fs.url(date)

    if User.objects.filter(username=email).exists():
        messages.error(request,'email/username already exists')
        return redirect('/myapp/admin_Addsubadmin/#abc')
    

    import random
    new_pass = random.randint(00000, 99999)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("leagaladvisorteam@gmail.com", " eugnxtyylwtqwlav")  # App Password
    to = email
    subject = "Test Email"
    body = "Your new password is " + str(new_pass)
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail("s@gmail.com", to, msg)  # Disconnect from the server
    server.quit()



    user=User.objects.create_user(username=email,password=str(new_pass))
    user.groups.add(Group.objects.get(name='Subadmin'))
    user.save()


    sobj = Subadmin()
    sobj.name = name
    sobj.DOB = DOB
    sobj.Gender = gender
    sobj.Email = email
    sobj.Phonenumber = Phonenumber
    sobj.DEPARTMENT_id= department
    sobj.Photo = path
    sobj.AUTH_USER=user
    sobj.save()
    messages.success(request, "Added Successfull")
    return redirect('/myapp/admin_Viewsubadmin/#abc')

@login_required(login_url='/myapp/login_get/')  
def admin_Viewsubadmin(request):
    res = Subadmin.objects.all()
    return render(request,'admin/View sub admin.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def admin_Editsubadmin(request,id):
    data = Subadmin.objects.get(id=id)
    res = Department.objects.all()
    return render(request,'admin/Edit sub admin.html',{'data':data,'dept':res})

@login_required(login_url='/myapp/login_get/')  
def admin_Editsubadmin_post(request):
    name=request.POST['name']
    DOB = request.POST['DOB']
    gender = request.POST['gender']
    email = request.POST['email']
    Phonenumber = request.POST['phonenumber']
    department = request.POST['department']
    id = request.POST['id']

    sobj = Subadmin.objects.get(id=id)
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        date = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        fs.save(date, photo)
        path = fs.url(date)
        sobj.Photo = path
        sobj.save()

    sobj.name = name
    sobj.DOB = DOB
    sobj.Gender = gender
    sobj.Email = email
    sobj.Phonenumber = Phonenumber
    sobj.DEPARTMENT_id = department
    sobj.save()
    messages.success(request, "Edited Successfull")
    return redirect('/myapp/admin_Viewsubadmin/#abc')

@login_required(login_url='/myapp/login_get/')  
def delete_subadmin(request,sid):
    Subadmin.objects.filter(id=sid).delete()
    messages.success(request,"Delete Successfull")
    return redirect('/myapp/admin_Viewsubadmin/#abc')

@login_required(login_url='/myapp/login_get/')  
def admin_Assignelectioncoordinator(request):
    res=Election.objects.all()
    staff=Staff.objects.all()
    return render(request,'admin/Assign Election Coordinator.html',{'data':res,'staff':staff})

@login_required(login_url='/myapp/login_get/')  
def admin_Assignelectioncoordinator_post(request):
    staff=request.POST['staff']
    election=request.POST['election']

    s = Staff.objects.get(id=staff)

    import random
    new_pass = random.randint(00000, 99999)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("leagaladvisorteam@gmail.com", " eugnxtyylwtqwlav")  # App Password
    to = s.Email
    subject = "Test Email"
    body = "Your new password is " + str(new_pass)
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail("s@gmail.com", to, msg)  # Disconnect from the server
    server.quit()


    if Electioncoordinator.objects.filter(Staff=staff).exists():
        messages.error(request, 'already you are a coordinator')
        print(1)
        return redirect('/myapp/admin_Assignelectioncoordinator/#abc')
    elif User.objects.filter(username=s.Email):
        messages.error(request, 'email already exist')
        print(2)
        return redirect('/myapp/admin_Assignelectioncoordinator/#abc')

    else:

        user = User.objects.create_user(username=s.Email, password=str(new_pass))
        user.groups.add(Group.objects.get(name='Electioncoordinator'))
        user.save()

        aobj = Electioncoordinator()
        aobj.Staff_id = staff
        aobj.ELECTION_id = election
        aobj.AUTH_USER = user
        aobj.save()
        messages.success(request, "Added Successfull")
        return redirect('/myapp/admin_viewelectioncoordinator/#abc')

@login_required(login_url='/myapp/login_get/')  
def admin_viewelectioncoordinator(request):
    res = Electioncoordinator.objects.all()
    return render(request,'admin/view election coordinator.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def admin_editelectioncoordinator(request,id):
    data = Electioncoordinator.objects.get(id=id)
    res = Election.objects.all()
    staff = Staff.objects.all()
    return render(request,'admin/edit election coordinator.html',{'data':data,'res':res,'staff':staff})

@login_required(login_url='/myapp/login_get/')  
def admin_editelectioncoordinator_post(request):
    staff = request.POST['staff']
    election = request.POST['election']
    id = request.POST['id']

    aobj = Electioncoordinator.objects.get(id=id)
    aobj.Staff = staff
    aobj.ELECTION = election
    aobj.save()
    messages.success(request, "edited Successfull")
    return redirect('/myapp/admin_viewelectioncoordinator/#abc')

@login_required(login_url='/myapp/login_get/')  
def delete_electioncoordinator(request,eid):
    Electioncoordinator.objects.filter(id=eid).delete()
    messages.success(request,"Delete Successfull")
    return redirect('/myapp/admin_viewelectioncoordinator/#abc')

@login_required(login_url='/myapp/login_get/')  
def admin_AddElection(request):
    res = Department.objects.all()
    return render(request,'admin/Add Election.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def admin_Addelection_post(request):
    election=request.POST['election']
    Date=request.POST['date']
    department=request.POST['department']
    eobj = Election()
    eobj.ElectionName = election
    eobj.ElectionDate = Date
    eobj.Department_id = department
    eobj.Status = 'pending'
    eobj.save()
    messages.success(request, "Added Successfull")
    return redirect('/myapp/admin_ViewElection/#abc')

@login_required(login_url='/myapp/login_get/')  
def admin_ViewElection(request):
    res = Election.objects.all()
    return render(request,'admin/View Election.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def admin_Editelection(request,id):
    data = Election.objects.get(id=id)
    res = Department.objects.all()
    return render(request,'admin/Edit election.html',{'data':data,'dept':res})

@login_required(login_url='/myapp/login_get/')  
def admin_editelection_post(request):
    election=request.POST['Election']
    date=request.POST['Date']
    department=request.POST['department']
    id=request.POST['id']
    eobj = Election.objects.get(id=id)
    eobj.ElectionName = election
    eobj.ElectionDate = date
    eobj.Department_id = department
    eobj.save()
    messages.success(request, "edited Successfull")
    return redirect('/myapp/admin_ViewElection/#abc')

@login_required(login_url='/myapp/login_get/')  
def delete_election(request,eid):
    Election.objects.filter(id=eid).delete()
    messages.success(request,"Delete Successfull")
    return redirect('/myapp/admin_ViewElection/#abc')

@login_required(login_url='/myapp/login_get/')  
def admin_viewnominees(request):
    res = Nominees.objects.all()
    return render(request,'admin/view nominees.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def admin_ViewStaff(request):
    res = Staff.objects.all()
    return render(request,'admin/View Staff.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def admin_viewstudent(request):
    res = Student.objects.all()
    return render(request,'admin/view student.html',{'data':res})



def admin_view_complaint_get(request):
    data = Complaint.objects.all()
    return render(request, "admin/view_complaint.html",{'data':data})

def admin_sentreply_get(request,id):
    return render(request, "admin/sentreply.html",{'id':id})
def admin_sentreply_post(request):
    reply = request.POST['reply']
    id = request.POST['id']
    data=Complaint.objects.get(id=id)
    data.reply_text=reply
    data.save()
    return redirect('/myapp/admin_view_complaint_get/')


# user=User.objects.get(username='admin@gmail.com')
# user.set_password(1234)
# user.save()



# ===========================================subadmin=================================


@login_required(login_url='/myapp/login_get/')  
def view_profile(request):
    d=request.user
    data=Subadmin.objects.get(AUTH_USER_id=d)
    return render(request,"subadmin/view profile.html",{"data":data})




def homesub_s(request):
    return render(request,'subadmin/subadmin_index.html')
    # return render(request,'subadmin/homesub.html')

@login_required(login_url='/myapp/login_get/')  
def Subadmin_Addstudent(request):
    res = Department.objects.all()
    return render(request,'subadmin/Add student.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def Subadmin_Addstudent_post(request):
    name=request.POST['name']
    DOB=request.POST['DOB']
    gender=request.POST['gender']
    email=request.POST['email']
    Phonenumber=request.POST['phonenumber']
    department=request.POST['department']
    Rollno=request.POST['Rollno']
    semester=request.POST['semester']
    photo=request.FILES['photo']

    fs = FileSystemStorage()
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    fs.save(date, photo)
    path = fs.url(date)

    if User.objects.filter(username=email).exists():
        messages.error(request, 'email/username already exists')
        return redirect('/myapp/Subadmin_Addstudent/#abc')
    
    import random
    new_pass = random.randint(00000, 99999)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("leagaladvisorteam@gmail.com", " eugnxtyylwtqwlav")  # App Password
    to = email
    subject = "Test Email"
    body = "Your new password is " + str(new_pass)
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail("s@gmail.com", to, msg)  # Disconnect from the server
    server.quit()

    user = User.objects.create_user(username=email, password=str(new_pass))
    user.groups.add(Group.objects.get(name='Student'))
    user.save()

    sobj = Student()
    sobj.name = name
    sobj.DOB = DOB
    sobj.Gender = gender
    sobj.Email = email
    sobj.Rollno = Rollno
    sobj.semester = semester
    sobj.Phonenumber = Phonenumber
    sobj.DEPARTMENT_id = department
    sobj.Photo = path
    sobj.AUTH_USER = user
    sobj.save()
    messages.success(request, "Added Successfull")
    return redirect('/myapp/subadmin_Viewstudent/#abc')


@login_required(login_url='/myapp/login_get/')  
def subadmin_Viewstudent(request):
    res = Student.objects.all()
    return render(request,'subadmin/View Student.html',{'data':res})


@login_required(login_url='/myapp/login_get/')  
def Subadmin_Editstudent(request,id):
    res = Department.objects.all()
    data1=Student.objects.get(id=id)
    return render(request,'subadmin/Edit student.html',{'data':res,'data1':data1})

@login_required(login_url='/myapp/login_get/')  
def Subadmin_Editstudent_post(request):
    id=request.POST['id']
    name=request.POST['name']
    DOB=request.POST['DOB']
    gender=request.POST['gender']
    email=request.POST['email']
    Phonenumber=request.POST['phonenumber']
    department=request.POST['department']
    Rollno=request.POST['Rollno']
    semester=request.POST['semester']

    sobj=Student.objects.get(id=id)

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        date = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        fs.save(date, photo)
        path = fs.url(date)
        sobj.Photo=path
        sobj.save()



    sobj.name = name
    sobj.DOB = DOB
    sobj.Gender = gender
    sobj.Email = email
    sobj.Rollno = Rollno
    sobj.semester = semester
    sobj.Phonenumber = Phonenumber
    sobj.DEPARTMENT_id = department
    sobj.save()
    messages.success(request, "Edited Successfull")
    return redirect('/myapp/subadmin_Viewstudent/#abc')

@login_required(login_url='/myapp/login_get/')  
def subadmindeletestudent(request,id):
    Student.objects.get(AUTH_USER_id=id).delete()
    User.objects.get(id=id).delete()
    return redirect('/myapp/subadmin_Viewstudent/#abc')

@login_required(login_url='/myapp/login_get/')  
def Subadmin_Addstaff(request):
    res = Department.objects.all()
    return render(request,'subadmin/Add Staff.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def Subadmin_Addstaff_post(request):
    name=request.POST['name']
    DOB=request.POST['DOB']
    gender=request.POST['gender']
    email=request.POST['email']
    Phonenumber=request.POST['phonenumber']
    department=request.POST['department']
    photo=request.FILES['photo']
    Id_proof=request.FILES['Id Proof']

    fs = FileSystemStorage()
    date = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    fs.save(date, photo)
    path = fs.url(date)

    date1 = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    fs.save(date1, Id_proof)
    path1 = fs.url(date1)

    sobj = Staff()
    sobj.name = name
    sobj.DOB = DOB
    sobj.Gender = gender
    sobj.Email = email
    sobj.Phonenumber = Phonenumber
    sobj.DEPARTMENT_id = department
    sobj.Photo = path
    sobj.idproof= path1
    sobj.save()
    messages.success(request, "Added Successfull")
    return redirect('/myapp/subadmin_Viewstaff/#abc')

@login_required(login_url='/myapp/login_get/')  
def subadmin_Viewstaff(request):
    res = Staff.objects.all()
    return render(request, 'subadmin/View Staff.html', {'data': res})

@login_required(login_url='/myapp/login_get/')  
def Subadmin_Editstaff(request,id):
    res = Department.objects.all()
    data1=Staff.objects.get(id=id)
    return render(request,'subadmin/Edit Staff.html',{'data':res,'data1':data1})

@login_required(login_url='/myapp/login_get/')  
def Subadmin_Editstaff_post(request):
    id=request.POST['id']
    name=request.POST['name']
    DOB=request.POST['DOB']
    gender=request.POST['gender']
    email=request.POST['email']
    Phonenumber=request.POST['phonenumber']
    department=request.POST['department']



    sobj=Student.objects.get(id=id)

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        date = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        fs.save(date, photo)
        path = fs.url(date)
        sobj.Photo=path
        sobj.save()

    if 'idproof' in request.FILES:
        Id_proof = request.FILES['Id Proof']
        fs1 = FileSystemStorage()
        date1 = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        fs1.save(date1, Id_proof)
        path1 = fs1.url(date1)
        sobj.idproof=path1
        sobj.save()


    sobj.name = name
    sobj.DOB = DOB
    sobj.Gender = gender
    sobj.Email = email
    sobj.Phonenumber = Phonenumber
    sobj.DEPARTMENT_id = department
    sobj.save()
    messages.success(request, "Edited Successfull")
    return redirect('/myapp/subadmin_Viewstaff/#abc')


@login_required(login_url='/myapp/login_get/')  
def subadmindeletestaff(request,id):
    Staff.objects.get(id=id).delete()
    return redirect('/myapp/subadmin_Viewstaff/#abc')

@login_required(login_url='/myapp/login_get/')  
def Subadmin_changepassword(request):
    return render(request,'Subadmin/Change password.html')

@login_required(login_url='/myapp/login_get/')  
def Subadmin_changepassword_post(request):
    enteroldpassword=request.POST['enter old password']
    enternewpassword=request.POST['enter new password']
    confirmpassword=request.POST['confirm password']
    user=request.user
    if user.check_password(enteroldpassword):
        if enternewpassword==confirmpassword:
            user.set_password(enternewpassword)
            user.save()
            return redirect('/myapp/login_get/')
        else:
            return redirect('/myapp/Subadmin_changepassword/#abc')
    else:
        return redirect('/myapp/Subadmin_changepassword/#abc')

@login_required(login_url='/myapp/login_get/')  
def Subadmin_ViewElection(request):
    res = Election.objects.all()
    return render(request,'Subadmin/View Election.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def Subadmin_viewnominees(request):
    res = Nominees.objects.all()
    return render(request,'Subadmin/view nominees.html',{'data':res})

@login_required(login_url='/myapp/login_get/')  
def Subadmin_viewresult(request):
    return render(request,'Subadmin/view Result.html')


#-------------------------------- C O O R D I N A T O R-------------------------------------------

@login_required(login_url='/myapp/login_get/')  
def coordinator_home(request):
    return render(request,'coordinator/coordinator_index.html')

@login_required(login_url='/myapp/login_get/')  
def coordinator_view_profile(request):
    d=request.user
    data=Electioncoordinator.objects.get(AUTH_USER_id=d)
    return render(request,"coordinator/view profile.html",{"data":data})

@login_required(login_url='/myapp/login_get/')  
def coordinator_view_ElectionStatus(request):
    data=Election.objects.all()
    return render(request,"coordinator/View Election Status.html",{"data":data})

@login_required(login_url='/myapp/login_get/')  
def coordinator_view_VerifyNominee(request,id):
    data = Nominees.objects.filter(ELECTION_id=id)
    return render(request, "coordinator/verify nomine.html", {"data": data})

@login_required(login_url='/myapp/login_get/')
def coordinator_approve_nominie(request,id):
    Nominees.objects.filter(id=id).update(status='approved')
    return redirect('/myapp/coordinator_view_VerifyNominee/')

@login_required(login_url='/myapp/login_get/')
def coordinator_reject_nominie(request,id):
    Nominees.objects.filter(id=id).update(status='rejected')
    return redirect('/myapp/coordinator_view_VerifyNominee/')


@login_required(login_url='/myapp/login_get/')
def coordinator_view_approved_Nominee(request):
    data = Nominees.objects.filter(status='approved')
    return render(request, "coordinator/approved nomine.html", {"data": data})

@login_required(login_url='/myapp/login_get/')
def coordinator_view_rejected_Nominee(request):
    data = Nominees.objects.filter(status='rejected')
    return render(request, "coordinator/rejected nomine.html", {"data": data})

@login_required(login_url='/myapp/login_get/')  
def coordinator_view_Result(request):
    return render(request, "coordinator/view result.html")


@login_required(login_url='/myapp/login_get/')  
def Coordinator_changepassword(request):
    return render(request,'Coordinator/Change password.html')

@login_required(login_url='/myapp/login_get/')  
def Coordinator_changepassword_post(request):
    enteroldpassword=request.POST['enter old password']
    enternewpassword=request.POST['enter new password']
    confirmpassword=request.POST['confirm password']
    user=request.user
    if user.check_password(enteroldpassword):
        if enternewpassword==confirmpassword:
            user.set_password(enternewpassword)
            user.save()
            return redirect('/myapp/login_get/')
        else:
            return redirect('/myapp/coordinator_changepassword/')

################################### STUDENT ###############################
@csrf_exempt
def Mobile_login(request):
    username = request.POST['Username']
    password = request.POST['Password']
    print(username, password)

    user = authenticate(request, username=username, password=password)
    print('hvjh', user)

    if user is not None:
        if user.groups.filter(name='student').exists():
            login(request, user)
            return JsonResponse({'status': 'ok', 'lid': str(user.id)})
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})


@csrf_exempt
def Student_dashboard(request):
    id= request.POST['lid']
    a=Student.objects.get(AUTH_USER_id=id)
    return JsonResponse({
        'status':'ok',
        'name':a.name,
        'Photo':a.Photo,
    })


@csrf_exempt
def StudentViewProfile(request):
    id= request.POST['lid']
    a=Student.objects.get(AUTH_USER_id=id)
    return JsonResponse({
        'status':'ok',
        'name':a.name,
        'dob':a.DOB,
        'Gender':a.Gender,
        'Email':a.Email,
        'Phonenumber':a.Phonenumber,
        'department':a.DEPARTMENT.department,
        'Rollno':a.Rollno,
        'semester':a.semester,
        'Photo':a.Photo,

    })



@csrf_exempt
def StudentViewElection(request):

    lid = request.POST['lid']
    student = Student.objects.get(AUTH_USER_id=lid)
    department_id = student.DEPARTMENT.id

    elections = Election.objects.filter(Department_id=department_id)
    data = []

    for election in elections:
        data.append({
            'eid': election.id,
            'ElectionName': election.ElectionName,
            'ElectionDate': str(election.ElectionDate),
            'Department': election.Department.department,
            'Status': election.Status,
        })

    if data:
        return JsonResponse({'status': 'ok', 'data': data})
    else:
        return JsonResponse({'status': 'no', 'message': 'No elections found for your department'})

@csrf_exempt
def student_send_nomination(request):
    sid=request.POST['lid']
    eid=request.POST['eid']
    
    a=Nominees()
    a.STUDENT=Student.objects.get(AUTH_USER_id=sid)
    a.ELECTION=Election.objects.get(id=eid)
    a.status='pending'
    a.save()
    return JsonResponse({'status':'ok'})

@csrf_exempt
def student_view_nomination(request):
    lid=request.POST['lid']
    data=Nominees.objects.filter(STUDENT__AUTH_USER_id=lid)
    l=[]
    for i in data:
        l.append(
            {
            'id': i.id,
            'ElectionName': i.ELECTION.ElectionName,
            'ElectionDate': str(i.ELECTION.ElectionDate),
            'Department': i.STUDENT.DEPARTMENT.department,
            'Status': i.status,
            }
        )
    return JsonResponse({'status': 'ok', 'data': l})



@csrf_exempt
def student_send_complaint(request):
    complaint = request.POST['complaint']
    lid = request.POST['lid']


    a = Complaint()
    a.complaint_text = complaint
    a.status = 'pending'
    a.reply = 'pending'
    a.date=datetime.now().today()
    a.STUDENT = Student.objects.get(AUTH_USER_id=lid)
    a.save()

    return JsonResponse({'status': 'ok'})



@csrf_exempt
def student_view_reply(request):
    lid=request.POST['lid']
    data=Complaint.objects.filter(STUDENT__AUTH_USER_id=lid)
    l=[]
    for i in data:
        l.append(
            {
                'id':i.id,
                'date':i.date,
                'status':i.status,
                'complaint':i.complaint_text,
                'reply':i.reply
            }
        )
    return JsonResponse({'status': 'ok','data':l})


@csrf_exempt
def android_forget_password_post(request):
    email = request.POST['email']
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email is required'})

    try:
        user = User.objects.get(username=email)
        print(email)

        # Generate new password
        new_pass = str(random.randint(1000, 9999))
        user.password = make_password(str(new_pass))
        user.save()

        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "trainingstarted@gmail.com"
        app_password = "nlxasujxgazlbmgz"

        subject = "Your New Password"
        body = f"Your new password is: {new_pass}"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(message)
        server.quit()

        return JsonResponse({'status': 'ok', 'message': 'Password sent to your email'})

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Email not found'})



@csrf_exempt
def student_view_candidates(request):
    eid=request.POST['eid']
    data=Nominees.objects.filter(status='approved',ELECTION_id=eid)
    l=[]
    for i in data:
        l.append(
            {
            'id': i.id,
            'ElectionName': i.ELECTION.ElectionName,
            'ElectionDate': str(i.ELECTION.ElectionDate),
            'Department': i.STUDENT.DEPARTMENT.department,
            'candidate': i.STUDENT.name,
            'photo': i.STUDENT.Photo,
            'Status': i.status,
            }
        )
    return JsonResponse({'status': 'ok', 'data': l})



@csrf_exempt
def StudentViewTodayElection(request):

    lid = request.POST['lid']
    student = Student.objects.get(AUTH_USER_id=lid)
    department_id = student.DEPARTMENT.id

    from datetime import datetime
    elections = Election.objects.filter(Department_id=department_id,ElectionDate=datetime.now().today())
    data = []

    for election in elections:
        data.append({
            'eid': election.id,
            'ElectionName': election.ElectionName,
            'ElectionDate': str(election.ElectionDate),
            'Department': election.Department.department,
            'Status': election.Status,
        })

    if data:
        return JsonResponse({'status': 'ok', 'data': data})
    else:
        return JsonResponse({'status': 'no', 'message': 'No elections found for your department'})





import os
import datetime
import cv2
import face_recognition
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .models import Student

@csrf_exempt
def check_face(request):
    try:
        lid = request.POST.get('lid')
        eid = request.POST.get('eid')
        uploaded_file = request.FILES.get('photo')
        print(uploaded_file, "📸 Uploaded file")

        # Uploaded image from Flutter
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        fs = FileSystemStorage(location=upload_dir)
        filename = fs.save(datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg", uploaded_file)
        uploaded_path = fs.path(filename)
        print("📂 Uploaded image saved at:", uploaded_path)

        if not lid or not uploaded_file:
            return JsonResponse({'status': 'no', 'message': 'Missing required data (lid/photo)'})

        print(f"🔍 Checking face for LID={lid}, EID={eid}")

        # ✅ Get student
        try:
            student = Student.objects.get(AUTH_USER__id=lid)
            print("✅ Student found:", student)
        except Student.DoesNotExist:
            return JsonResponse({'status': 'no', 'message': 'Student not found'})

        # ✅ Known photo
        # Remove leading /media/ if present
        photo_rel_path = student.Photo
        if photo_rel_path.startswith("media/") or photo_rel_path.startswith("/media/"):
            photo_rel_path = photo_rel_path.split("media/", 1)[1]

        # Now join with MEDIA_ROOT
        known_photo_path = os.path.join(settings.MEDIA_ROOT, photo_rel_path)
        known_photo_path = os.path.abspath(known_photo_path)

        print("🖼 Known photo path:", known_photo_path, "| Exists:", os.path.exists(known_photo_path))

        if not os.path.exists(known_photo_path):
            return JsonResponse({'status': 'no', 'message': 'Student photo not found on server'})

        # ✅ Encode known image
        known_img = face_recognition.load_image_file(known_photo_path)
        known_encodings = face_recognition.face_encodings(known_img)
        print("Known encodings found:", len(known_encodings))

        if not known_encodings:
            return JsonResponse({'status': 'no', 'message': 'No recognizable face in student photo'})
        known_encoding = known_encodings[0]

        # ✅ Save uploaded photo
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        fs = FileSystemStorage(location=upload_dir)
        filename = fs.save(datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg", uploaded_file)
        uploaded_path = fs.path(filename)
        print("📂 Uploaded image saved at:", uploaded_path)

        # ✅ Read uploaded image
        frame = cv2.imread(uploaded_path)
        if frame is None:
            return JsonResponse({'status': 'no', 'message': 'Error reading uploaded image'})

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        unknown_encodings = face_recognition.face_encodings(rgb_frame)
        print("Unknown encodings found:", len(unknown_encodings))

        if not unknown_encodings:
            return JsonResponse({'status': 'no', 'message': 'No face detected in uploaded image'})
        if len(unknown_encodings) > 1:
            return JsonResponse({'status': 'no', 'message': 'Multiple faces detected — please retake photo'})

        # ✅ Compare faces with tolerance sweep
        match_strict = face_recognition.compare_faces([known_encoding], unknown_encodings[0], tolerance=0.45)[0]
        match_normal = face_recognition.compare_faces([known_encoding], unknown_encodings[0], tolerance=0.55)[0]
        match_loose = face_recognition.compare_faces([known_encoding], unknown_encodings[0], tolerance=0.65)[0]

        print(f"Match results → strict(0.45): {match_strict}, normal(0.55): {match_normal}, loose(0.65): {match_loose}")

        photo_url = request.build_absolute_uri(fs.url(filename))

        if match_normal or match_loose:
            return JsonResponse({'status': 'ok', 'message': 'Face matched successfully', 'photo_path': photo_url})
        else:
            return JsonResponse({'status': 'no', 'message': 'Face did not match', 'photo_path': photo_url})

    except Exception as e:
        print("❌ Error in check_face:", str(e))
        return JsonResponse({'status': 'no', 'message': f'Error: {e}'})
