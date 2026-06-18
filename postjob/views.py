from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.contrib import messages
from postjob.models import PostJob, ApplyJob
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
class PostJobView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'post_job.html')

    def post(self, request):
        next_page = request.GET.get('next')
        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        category = request.POST.get('category')
        minimum_salary = request.POST.get('minimum_salary')
        maximum_salary = request.POST.get('maximum_salary')
        job_description = request.POST.get('job_description')
        application_email = request.POST.get('application_email')
        if not job_title or not company_name or not location or not job_type or not category or not minimum_salary or not maximum_salary or not job_description or not application_email:
            messages.error(request, 'All fields are required.')
            return render(request, 'post_job.html')

        if len(job_description) < 50:
            messages.error(request, 'Job description must be at least 50 characters.')
            return render(request, 'post_job.html')

        try:
            minimum_salary = int(minimum_salary)
            maximum_salary = int(maximum_salary)
        except ValueError:
            messages.error(request, 'Salary must be a valid number.')
            return render(request, 'post_job.html')

        if minimum_salary >= maximum_salary:
            messages.error(request, 'Minimum salary must be less than maximum salary.')
            return render(request, 'post_job.html')

        PostJob.objects.create(job_title = job_title,
                                company_name = company_name,
                                location = location,
                                job_type = job_type,
                                category = category,
                                minimum_salary = minimum_salary,
                                maximum_salary = maximum_salary,
                                job_description = job_description,
                                application_email = application_email,
                                user=request.user,

        )
        messages.success(request, 'Job posted successfully! It will go live after review.')
        return redirect(next_page or resolve_url('home'))


class EditJobView(LoginRequiredMixin, View):
    def get(self, request, job_id):
        editjob = PostJob.objects.filter(id=job_id).first()
        if not editjob:
            return redirect(resolve_url('find_job'))
        if editjob.user != request.user:
             return redirect(resolve_url('find_job'))
        context = {"editjobview" : editjob}
        return render(request, 'edit_job.html', context)

    def post(self, request, job_id):
        editjob = PostJob.objects.filter(id=job_id).first()
        if not editjob:
            return redirect(resolve_url('find_job'))
        if editjob.user != request.user:
            return redirect(resolve_url('find_job'))

        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        category = request.POST.get('category')
        minimum_salary = request.POST.get('minimum_salary')
        maximum_salary = request.POST.get('maximum_salary')
        job_description = request.POST.get('job_description')
        application_email = request.POST.get('application_email')

        editjob.job_title = job_title or editjob.job_title
        editjob.company_name = company_name or editjob.company_name
        editjob.location = location or editjob.location
        editjob.job_type = job_type or editjob.job_type
        editjob.category = category or editjob.category
        editjob.minimum_salary = minimum_salary or editjob.minimum_salary
        editjob.maximum_salary = maximum_salary or editjob.maximum_salary
        editjob.job_description = job_description or editjob.job_description
        editjob.application_email = application_email or editjob.application_email
        editjob.save()
        messages.success(request, 'Job successfully updated, It will go live after review.')
        return redirect(resolve_url('find_job'))

@login_required
def deletejob(request, job_id):
    deletejob = PostJob.objects.filter(id=job_id).first()
    if not deletejob:
        return redirect(resolve_url('find_job'))
    if deletejob.user != request.user:
        return redirect(resolve_url('find_job'))

    deletejob.delete()
    messages.success(request, 'Job successfully deleted.')
    return redirect(resolve_url('find_job'))


@login_required
def applyjob(request, job_id):
    applyjob = PostJob.objects.filter(id=job_id).first()
    if not applyjob:
        messages.error(request, 'Job not found')
        return redirect(resolve_url('find_job'))
    if applyjob.user == request.user:
        messages.error(request, 'You are the job owner!!')
        return redirect(resolve_url('find_job'))
    
    if request.method == 'POST':
        fullname = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cover_letter = request.POST.get('cover_letter')
        cv = request.FILES.get('cv')
        if not fullname or not email or not phone or not cover_letter or not cv:
            messages.error(request, 'All fields are required.')
            return render(request, 'apply.html', {'job': applyjob})
        if '@' not in email or '.' not in email:
            messages.error(request, 'Enter a valid email address.')
            return render(request, 'apply.html', {'job': applyjob})
        if len(phone) < 11:
            messages.error(request, 'Enter a valid phone number.')
            return render(request, 'apply.html', {'job': applyjob})
        if len(cover_letter) < 200:
            messages.error(request, 'Cover letter must be at least 200 characters.')
            return render(request, 'apply.html', {'job': applyjob})
        allowed = ['.pdf', '.doc', '.docx']
        if not any(cv.name.lower().endswith(ext) for ext in allowed):
            messages.error(request, 'CV must be PDF, DOC or DOCX.')
            return render(request, 'apply.html', {'job': applyjob})
        if cv.size > 5 * 1024 * 1024:
            messages.error(request, 'CV file size must not exceed 5MB.')
            return render(request, 'apply.html', {'job': applyjob})
    
        already_applied = ApplyJob.objects.filter(job=applyjob, applicant=request.user).exists()
        if already_applied:
            messages.success(request, 'You have already applied for this job.')
            return redirect('job_detail', id=applyjob.id)
    
        ApplyJob.objects.create(job=applyjob, applicant=request.user, full_name=fullname, email=email, phone=phone, cv=cv, cover_letter=cover_letter)
        messages.success(request, f'Application submitted successfully for {applyjob.job_title}!')
        return redirect('job_detail', id=applyjob.id)
    
    return render(request, 'apply.html', {'job': applyjob})
    

 