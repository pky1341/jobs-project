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
import requests
from django_countries import countries
from django.forms import ValidationError
from django.views.generic import TemplateView
# Create your views here.


class Home(TemplateView):
    template_name = "index.html"
def index(request):
    return render(request,'index.html')
def job_listing(request):
    return render(request,'job_listing.html')
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
            user_name=request.POST['user_name']
            email=request.POST['mail']
            password=request.POST['passwd']
            c_password=request.POST['cpasswd']
            values={
            'user_name':user_name,
            'email':email,
            'password':password,
            'c_password':c_password
            }
            err=None
            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
            if not (email and password):
                err="all field are required"
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
            user_m=UserMaster(username=user_name,password=password,email=email)
            user_m.save()
            can=Candidate(user_id=user_m)
            can.save()
            myuser=User.objects.create_user(username=user_name,email=email,password=password)
            myuser.save()
            messages.success(request,"your account has been succcessfully created...now you needs login..")
            return redirect('/signup')
        return render(request,"register.html")
    except Http404:
        return HttpResponseNotFound("page not found")    
def signin(request):
    try:
        if request.method=="POST":
            email=request.POST['mail']
            password=request.POST['passwd']
            user_m=UserMaster.objects.get(email=email)
            if user_m:
                user_n=user_m.username
            if Candidate.objects.get(user_id=user_m):
                myuser=authenticate(request,username=user_n,email=email,password=password)
                if myuser is not None:
                    login(request,myuser)
                    can=User.objects.get(email=email)
                    firstname=can.first_name
                    lastname=can.last_name
                    email=can.email
                    context={
                    'lastname':lastname,
                    'firstname':firstname,
                    'email':email
                    }    
                    request.session["firstname"]=can.first_name
                    request.session["lastname"]=can.last_name
                    request.session["id"]=request.POST['mail']
                    return render(request,"index.html",context)
                else:
                    messages.warning(request,"Do not match your entered password...")
                    return render(request,"login.html")
            else:
                messages.warning(request,'you are not Candidate')
                return render(request,'login.html')
        else:
            # messages.warning(request,"your method not post method")
            return render(request,"login.html")
    except ValueError as e:
        raise e
def OTPpage():
    pass
def signout(request):
    if request.session.has_key('id'):
        logout(request)
        # del request.session["role"]
        # del request.session["firstname"]
        # del request.session['lastname']
        # del request.session["id"]
        messages.warning(request,"please complete login otherwise not access any page")
        return render(request,"login.html")
    else:
        return render(request,"login.html")
def user_profile(request):
    if request.session.has_key('id'):
        pk=request.session['id']
        user=UserMaster.objects.get(email=pk)
        email=user.email
        context={
        'email':email,
        'countries':countries,
        }
        return render(request,"user_profile.html",context)
    else:
        return render(request,"login.html")
def  p_update(request):
    pk=request.session['id']
    # print(pk)
    if pk:
        user_m=UserMaster.objects.get(email=pk)
        can=Candidate.objects.get(user_id=user_m)
        user=User.objects.get(email=pk)
        if can:
            if request.method=='POST':
                can.firstname=request.POST['fname']
                can.lastname=request.POST['lname']
                user_m.email=request.POST['email']
                can.contact=request.POST['contact']
                can.state=request.POST['state']
                can.city=request.POST['city']
                can.address=request.POST['addr']
                can.dob=request.POST['dob']
                can.gender=request.POST['a']
                can.pin=request.POST['pincode']
                can.education=request.POST['education']
                can.experince=request.POST['experince']
                can.country=request.POST['country']
                can.skill=request.POST['skill']
                can.annual_pay=request.POST['salary']
                can.language=request.POST['lang']
                can.bio=request.POST['bio']
                can.resume=request.FILES['resume']
                can.profile_pic=request.FILES['photo']
                values={
                'contact':can.contact,
                'city':can.city,
                'state':can.state,
                'address':can.address,
                'dob':can.dob,
                'gender':can.gender,
                'pin':can.pin,
                'experince':can.experince,
                "education":can.education,
                'country':can.country,
                'skill':can.skill,
                'annual_pay':can.annual_pay,
                'language':can.language,
                'bio':can.bio,
                'resume':can.resume,
                'profile_pic':can.profile_pic
                }
                err=None
                context={}
                    # pattern = r'^\d{3}-\d{3}-\d{4}$'
                if len(can.contact)!=10:
                    err="Oops! The contact number should have exactly 10 digits."
                if not (can.contact).isdigit():
                    err="Oops! The contact number should only contain numeric digits."
                    # if re.match(pattern,(can.contact)):
                    #     err="Oops! The contact number is in an incorrect format."
                if not can.state:
                    err="State name is required."
                if len(can.state)<2 and len(can.state)>50:
                    err="State name should be between 2 and 50 characters."
                if not re.match(r'^[A-Za-z0-9\s\.,?!]+$',can.state):
                    err="State name should contain only alphabetic characters."
                if can.state.isspace():
                    err="spaces are not allowed"
                if not can.city:
                    err="city name is required."
                if len(can.city)<2 and len(can.city)>50:
                    err="city name should be between 2 and 50 characters."
                if not re.match(r'^[A-Za-z0-9\s\.,?!]+$',can.city):
                    err="city name should contain only alphabetic characters."
                if (can.city).isspace():
                    err="spaces are not allowed"
                if not can.address:
                    err="address is required."
                if len(can.address)<2 and len(can.address)>50:
                    err="address should be between 2 and 50 characters."
                if not re.match(r'^[A-Za-z0-9\s\.,?!]+$',can.address):
                    err="address should contain only alphabetic characters."
                if (can.address).isspace():
                    err="spaces are not allowed"
                if not can.dob:
                    err="date of birth is required"
                if len(can.pin)!=6:
                    err="Oops! PIN code should be 6 digits long!!!!"
                if not can.education:
                    err="Oops!! your highest education is required!!!!"
                if not (can.education).isalpha():
                    err="Oops!!education should contain only characters!!.."
                if (can.education).isspace():
                    err="education are not allowed spaces!!!"
                if request.POST['experince']=="Select experience level":
                    err="please select your work experience!!!"
                if request.POST['country']=="======select country======":
                    err="please select your country name!!!"
                if not re.match( r'^[A-Za-z0-9\s\.,?!]+$',(can.skill)):
                    err="skills should contain only alphabetic characters."
                if (can.skill).isspace():
                    err="only spaces are not allowed"
                if not re.match( r'^[A-Za-z0-9\s\.,?!]+$',(can.bio)):
                    err="Invalid bio format."
                if (can.bio).isspace():
                    err="only spaces are not allowed"
                user.first_name=can.firstname
                user.last_name=can.lastname
                if err:
                    context['values']=values
                    context['err']=err
                    context['firstname']=can.firstname
                    context['lastname']=can.lastname
                    context['email']=user_m.email
                    return render(request,"user_profile.html",context)
                else:
                    user.save()
                    can.save()
                    messages.success(request,"your account succcessfully updated...!!")
                    # ph_num=Candidate.objects.get(user_id=user_m)
                    # request.session['number']=ph_num.contact
                    return redirect('/c-profile')   
def c_profile(request):
    if request.session.has_key('id'):
        pk=request.session['id']
        if pk:
            user_m=UserMaster.objects.get(email=pk)
            cand=Candidate.objects.get(user_id=user_m)
            context={}
            context['user_m']=user_m
            context['cand']=cand
            return render(request,'c_profile.html',context)
    else:
        return render(request,'login.html')
def edit(request):
    if request.session.has_key('id'):
        pk=request.session['id']
        user_m=UserMaster.objects.get(email=pk)
        cand=Candidate.objects.get(user_id=user_m)
        if user_m:
            data={}            
            data['email']=user_m.email
            data['password']=user_m.password
            data['firstname']=cand.firstname
            data['lastname']=cand.lastname
            data['contact']=cand.contact
            data['state']=cand.state
            data['city']=cand.city
            data['address']=cand.address
            data['dob']=cand.dob
            data['pincode']=cand.pin
            data['education']=cand.education
            data['experince']=cand.experince
            data['country']=cand.country
            data['skill']=cand.skill
            data['annual_pay']=cand.annual_pay
            data['language']=cand.language
            data['bio']=cand.bio
            data['resume']=cand.resume
            data['photo']=cand.profile_pic
            return render(request,'edit.html',data)
        return render(request,"edit.html")
    else:
        return  render(request,"login.html")
def editable(request):
    pk=request.session['id']
    if pk:
        user_m=UserMaster.objects.get(email=pk)
        cand=Candidate.objects.get(user_id=user_m)
        if user_m:
            if request.method=='POST':
                user_m.email=request.POST['email']
                user_m.password=request.POST['passwd']
                cand.firstname=request.POST['fname']
                cand.lastname=request.POST['lname']
                cand.contact=request.POST['contact']
                cand.state=request.POST['state']
                cand.city=request.POST['city']
                cand.address=request.POST['addr']
                cand.dob=request.POST['dob']
                cand.pincode=request.POST['pincode']
                cand.education=request.POST['education']
                cand.experince=request.POST['experince']
                cand.country=request.POST['country']
                cand.skill=request.POST['skill']
                cand.annual_pay=request.POST['except']
                cand.language=request.POST['language']
                cand.bio=request.POST['bio']
                cand.resume=request.POST['resume']
                cand.profile_pic=request.POST['photo']
                user_m.save()
                cand.save()
                messages.success(request,'your changes succcessfully done')
                return redirect('/')
def github_login(request):
    return  render(request,"index.html")
def com_register(request):
    if request.method=="POST":
        user_name=request.POST['user_name']
        email=request.POST['mail']
        password=request.POST['passwd']
        c_password=request.POST['cpasswd']
        values={
        'user_name':user_name,
        'email':email ,
        'password':password,
        'c_password':c_password
        }
        err=None
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not (comp_name and email and password):
            err="all field are required"
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
            return render(request,"company_register.html",data)
        user_m=UserMaster(username=user_name,password=password,email=email)
        user_m.save()
        com=Company(user_id=user_m)
        com.save()
        myuser=User.objects.create_user(username=user_name,email=email,password=password)
        myuser.save()

        messages.success(request,"your account has been succcessfully created...now you needs login..")
        return redirect('/com_register')
    return render(request,'company_register.html')
def com_login(request):
    if request.method=="POST":
        email=request.POST['mail']
        password=request.POST['passwd']
        user_m=UserMaster.objects.get(email=email)
        if user_m:
            user_n=user_m.username
        if Company.objects.get(user_id=user_m):
            myuser=authenticate(request,username=user_n,email=email,password=password)
            if myuser is not None:
                login(request,myuser)
                com=User.objects.get(email=email)
                request.session["firstname"]=com.first_name
                request.session["lastname"]=com.last_name
                request.session["id"]=request.POST['mail']
                return redirect('/')    
            else:
                messages.warning(request,"Do not match your entered password...")
                return render(request,"com_login.html")
        else:
            messages.warning(request,'you are not Company...')
            return render(request,"com_login.html")
    else:
        # messages.warning(request,"your method not post method")
        return render(request,"com_login.html")        
    return render(request,'com_login.html')