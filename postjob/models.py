from django.db import models
import uuid
from django.contrib.auth.models import User



# Create your models here.
class PostJob(models.Model):
    id = models.UUIDField(default = uuid.uuid4, primary_key=True, editable=False)
    job_title = models.CharField(max_length = 250)
    company_name = models.CharField(max_length = 250)
    location = models.CharField(max_length = 250)
    job_type = models.CharField(max_length = 250)
    category = models.CharField(max_length = 250)
    minimum_salary = models.PositiveBigIntegerField()
    maximum_salary = models.PositiveBigIntegerField()
    job_description = models.TextField()
    application_email = models.EmailField()
    attended_to = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__ (self):
        return f'Job Title: {self.job_title}; Company Name: {self.company_name}'

    class Meta:
        ordering = ['-created_at']

class ApplyJob(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    job = models.ForeignKey(PostJob, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cv = models.FileField(upload_to='all_cvs/')
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    def __str__ (self):
        return f'Applicant name: {self.full_name}; Email: {self.email}'

    class Meta:
        unique_together = ('job', 'applicant')
