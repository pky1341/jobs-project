from django.db import models
# from django.contrib.auth.models import AbstractUser



# Create your models here.
class UserMaster(models.Model):
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    otp=models.IntegerField(blank=True,null=True)
    role=models.CharField(max_length=250)
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    is_created=models.DateTimeField(auto_now_add=True)
    is_updated=models.DateTimeField(auto_now_add=True)


class Candidate(models.Model):
    user_id=models.ForeignKey(UserMaster,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    address=models.CharField(max_length=250)
    dob=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    pin=models.IntegerField(null=False,default=0,auto_created=True)
    education=models.CharField(max_length=500)
    country=models.CharField(max_length=50)
    profile_pic=models.ImageField(upload_to="jobs_app/img/candidate")

class Company(models.Model):
    user_id=models.ForeignKey(UserMaster,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    company_name=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    address=models.CharField(max_length=250)
    contact=models.CharField(max_length=50)
    pin=models.IntegerField(null=False,default=0,auto_created=True)
    education=models.CharField(max_length=500)
    country=models.CharField(max_length=50)
    logo_pic=models.ImageField(upload_to="jobs_app/img/company")
    
    