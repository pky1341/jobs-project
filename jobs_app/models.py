from django.db import models
# from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserMaster(models.Model):
    username=models.CharField(max_length=50,default='',unique=True)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    otp=models.IntegerField(blank=True,null=True)
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    is_created=models.DateTimeField(auto_now_add=True)
    is_updated=models.DateTimeField(auto_now_add=True)
        

class Candidate(models.Model):
    user_id=models.ForeignKey(UserMaster,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    contact=models.CharField(max_length=50,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    address=models.TextField(max_length=300,null=True,blank=True)
    dob=models.DateField(max_length=50,null=True,auto_now_add=True,blank=True)
    gender=models.CharField(max_length=50,null=True,blank=True)
    pin=models.IntegerField(null=True,blank=True,default=0,auto_created=True)
    education=models.CharField(max_length=500,null=True,blank=True)
    experince=models.CharField(max_length=100,null=True,blank=True)
    country=models.CharField(max_length=50,null=True,blank=True)
    skill=models.TextField(editable=True,null=True,blank=True,error_messages={
            'unique': 'A candidate with this skill already exists.'
        })
    annual_pay=models.BigIntegerField(null=True,blank=True,default=0,help_text="enter annual salary")
    language=models.CharField(max_length=100,null=True,blank=True)
    bio=models.TextField(max_length=500,null=True,blank=True,help_text="Enter the main content of the for your bio")
    resume=models.FileField(upload_to="jobs_app/resume/Candidate",null=True,blank=True,default=None,help_text="Upload your resume in PDF format.")
    profile_pic=models.ImageField(upload_to="jobs_app/img/candidate",null=True,blank=True)

class Company(models.Model):
    user_id=models.ForeignKey(UserMaster,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=50,default='',null=True,blank=True)
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    job_title = models.CharField(max_length=100,default='',null=True,blank=True)
    department = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    responsibilities = models.TextField(null=True,blank=True)
    requirements = models.TextField(null=True,blank=True)
    qualifications = models.CharField(max_length=200,null=True,blank=True)
    experience = models.IntegerField(null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    employment_type = models.CharField(max_length=20, choices=JOB_TYPES,null=True,blank=True)
    salary = models.DecimalField(max_digits=8,null=True,blank=True, decimal_places=2)
    benefits = models.TextField(null=True,blank=True)
    skills = models.ManyToManyField('Skill')
    start_date = models.DateField(auto_now_add=True,null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    last_updated = models.DateTimeField(auto_now=True,null=True,blank=True)
    def __str__(self):
        return self.job_title


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    