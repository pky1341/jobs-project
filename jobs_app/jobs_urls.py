from django.urls import path,include
from jobs_app import views
from django_email_verification import urls as mail_urls
urlpatterns=[
    path('',views.index,name='home'),
    path('job_listing',views.job_listing,name="job_list"),
    path('about',views.about,name="about"),
    path('bloggs',views.blogg,name="blogg"),
    path('single-blog',views.single_blog,name="single-blog"),
    path('elements',views.element,name="elements"),
    path('job-details',views.job_detail,name="job-details"),
    path('contact',views.contact,name="contact"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('otp_page',views.OTPpage,name="otp_page"),
    path('signout',views.signout,name="signout"),
    path('user_profile',views.user_profile,name="user_profile")  
]