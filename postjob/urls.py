from django.urls import path
from postjob.views import PostJobView, EditJobView, deletejob, applyjob

urlpatterns = [
    path('postjob/', PostJobView.as_view(), name='post_job'),
    path('edit/<uuid:job_id>/', EditJobView.as_view(), name='edit_job'),
    path ('delete/<uuid:job_id>/', deletejob, name='delete_job'),
    path('apply/<uuid:job_id>/', applyjob, name='apply_job'), 
]
