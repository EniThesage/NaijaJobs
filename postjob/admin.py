from django.contrib import admin
from postjob.models import PostJob, ApplyJob

# Register your models here.
admin.site.register(PostJob),
admin.site.register(ApplyJob)
