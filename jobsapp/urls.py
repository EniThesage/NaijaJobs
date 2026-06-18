from django.urls import path
from jobsapp.views import homepage, joblisting, aboutpage, jobdetail


urlpatterns = [
 path('', homepage, name='home'),
 path('findjob/', joblisting, name='find_job'),
 path('about/', aboutpage, name='about'),
 path('findjob/<uuid:id>/', jobdetail, name='job_detail')
]
