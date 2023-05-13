from django.shortcuts import render,redirect
from jobs_app.models import UserMaster,Company,Candidate
from random import randint
from django.http import HttpResponseNotFound,Http404,JsonResponse,HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model,authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re

# Create your views here.
def index(request):
    if request.session.has_key('id'):
        return render(request,'index.html')
    else:
        return redirect('signin')
def job_listing(request):
    if request.session.has_key('id'):
        return render(request,'job_listing.html')
    else:
        return redirect('signin')
def about(request):
    if request.session.has_key('id'):
        return render(request,'about.html')
    else:
        return redirect('signin')
def blogg(request):
    if request.session.has_key('id'):
        return render(request,'blog.html')
    else:
        return redirect('signin')
def single_blog(request):
    if request.session.has_key('id'):
        return render(request,'single-blog.html')
    else:
        return redirect('signin')
def element(request):
    if request.session.has_key('id'):
        return render(request,'elements.html')
    else:
        return redirect('signin')
def job_detail(request):
    if request.session.has_key('id'):
        return render(request,'job_details.html')
    else:
        return redirect('signin')
def contact(request):
    if request.session.has_key('id'):
        return render(request,'contact.html')
    else:
        return redirect('signin')

def signup(request):
    try:
        if request.method=="POST":
            if request.POST['role']=="Candidate":
                role=request.POST['role']
                firstname=request.POST['fname']
                lastname=request.POST['lname']
                email=request.POST['mail']
                password=request.POST['passwd']
                c_password=request.POST['cpasswd']
                values={
                'fname':firstname,
                'lname':lastname,
                'role':role,
                'email':email,
                'password':password,
                'c_password':c_password
                }
                err=None
                pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
                if not (role and firstname and lastname and email and password):
                    err="all field are required"
                elif len(firstname) < 3:
                    err="First name should be at least 2 characters long "
                elif not re.match(r'^[a-zA-Z ]+$',firstname):
                    err="First name should only contain letters and spaces."
                elif firstname.isspace():
                    err="Invalid first name. Spaces are not allowed."
                elif len(lastname) < 3:
                    err="last name should be at least 2 characters long  "
                elif not re.match(r'^[a-zA-Z ]+$',lastname):
                    err="last name should only contain letters and spaces."
                elif lastname.isspace():
                    err="Invalid first name. Spaces are not allowed."
                elif len(password)<8:
                    err="Password must be 8 characters long "
                elif not re.match(pattern,password):
                    err="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character "
                elif password!=c_password:
                    err="password do not match "
                elif UserMaster.objects.filter(email=email).exists():
                    err="This email address is already taken "
                data={}
                data['error']=err
                data['values']=values
                if err:
                    return render(request,"register.html",data)
                user_m=UserMaster(role=role,password=password,email=email)
                user_m.save()
                can=Candidate(user_id=user_m,firstname=firstname,lastname=lastname)
                can.save()
                myuser=User.objects.create_user(username=email,email=email,first_name=firstname,last_name=lastname,password=password)
                myuser.save()
                messages.success(request,"your account has been succcessfully created...now you needs login..")
                return redirect('signin')
            elif request.POST['role']=="Company":
                role=request.POST['role']
                firstname=request.POST['fname']
                lastname=request.POST['lname']
                email=request.POST['mail']
                password=request.POST['passwd']
                c_password=request.POST['cpasswd']
                values={
                'fname':firstname,
                'lname':lastname,
                'role':role,
                'email':email,
                'password':password,
                'c_password':c_password
                }
                err=None
                pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
                if not (role and firstname and lastname and email and password):
                    err="all field are required"
                elif len(firstname) < 3:
                    err="First name should be at least 2 characters long "
                elif not re.match(r'^[a-zA-Z ]+$',firstname):
                    err="First name should only contain letters and spaces."
                elif firstname.isspace():
                    err="Invalid first name. Spaces are not allowed."
                elif len(lastname) < 3:
                    err="last name should be at least 2 characters long  "
                elif not re.match(r'^[a-zA-Z ]+$',lastname):
                    err="last name should only contain letters and spaces."
                elif lastname.isspace():
                    err="Invalid first name. Spaces are not allowed."
                elif len(password)<8:
                    err="Password must be 8 characters long "
                elif not re.match(pattern,password):
                    err="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character "
                elif password!=c_password:
                    err="password do not match "
                elif UserMaster.objects.filter(email=email).exists():
                    err="This email address is already taken "
                data={}
                data['error']=err
                data['values']=values
                if err:
                    return render(request,"register.html",data)
                user_m=UserMaster(role=role,password=password,email=email)
                user_m.save()
                com=Candidate(user_id=user_m,firstname=firstname,lastname=lastname)
                com.save()
                myuser=User.objects.create_user(username=email,email=email,first_name=firstname,last_name=lastname,password=password)
                myuser.save()

                messages.success(request,"your account has been succcessfully created...now you needs login..")
                return redirect('signin')
            else:
                messages.warning(request,"please select your role!!!")
                return render(request,"register.html")
        return render(request,"register.html")
    except Http404:
        return HttpResponseNotFound("page not found")    
def signin(request):
    try:
        if request.method=="POST":
            if request.POST['role']=="Candidate":
                role=request.POST['role']
                email=request.POST['mail']
                password=request.POST['passwd']
                myuser=authenticate(username=email,password=password)
                if myuser is not None:
                    login(request,myuser)
                    can=User.objects.get(email=email)    
                    request.session["role"]=request.POST["role"]
                    request.session["firstname"]=can.first_name
                    request.session["lastname"]=can.last_name
                    request.session["id"]=request.POST['mail']
                    return redirect('/')
                else:
                    messages.warning(request,"Incorrect your entered password...")
                    return render(request,"login.html")
            elif request.POST['role']=="Company":
                role=request.POST['role']
                email=request.POST['mail']
                password=request.POST['passwd']
                myuser=authenticate(username=email,password=password)
                if myuser is not None:
                    login(request,myuser)
                    com=User.objects.get(email=email)
                    request.session['role']=request.POST["role"]
                    request.session["firstname"]=com.first_name
                    request.session["lastname"]=com.last_name
                    request.session["id"]=request.POST['mail']
                    return redirect('/')    
                else:
                    messages.warning(request,"Incorrect your entered password...")
                    return render(request,"login.html")
            else:
                messages.warning(request,"please select your role!!!")
                return render(request,"login.html")
        else:
            # messages.warning(request,"your method not post method")
            return render(request,"login.html")
    except ValueError as e:
        raise e
def OTPpage():
    pass
def signout(request):
    if request.session.has_key('id'):
        del request.session["role"]
        del request.session["firstname"]
        del request.session['lastname']
        del request.session["id"]
        messages.warning(request,"please complete login otherwise not access any page")
        return render(request,"login.html")
    else:
        return render(request,"login.html")
def user_profile(request):
    if request.session.has_key('id'):
        return render(request,"user_profile.html")
    else:
        return render(request,"login.html")
    