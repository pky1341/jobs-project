from django.contrib import admin

from .models import UserMaster,Candidate,Company
# Register your models here.
admin.site.register(UserMaster)

class UserMasterAdmain(admin.ModelAdmin):
    list_display=['email','password','otp','role','is_active','is_verified','is_created','is_updated']
admin.site.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display=['user_id','firstname','lastname','contact','state','city','address','dob','gender','profile_pic']
admin.site.register(Company)
class ComapanyAdmin(admin.ModelAdmin):
    list_display=['emuser_id','firstname','lastname','company_name','state','city','address','contact','logo_pic']