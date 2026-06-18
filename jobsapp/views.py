from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.contrib import messages
from jobsapp.models import ContactMessages
from django.contrib.auth.decorators import login_required
from postjob.models import PostJob, ApplyJob
from django.db.models import Count, Q

# Create your views here.
def homepage(request):
    featured_jobs = PostJob.objects.all().order_by('-created_at')[:4]
    company_count = PostJob.objects.values('company_name').distinct().count()

    category_counts = (
        PostJob.objects
        .values('category')
        .annotate(total=Count('id'))
        )

    context = {
        'featured_jobs': featured_jobs,
        'job_count': PostJob.objects.count(),
        'category_counts': category_counts,
        'company_count': PostJob.objects.values('company_name').distinct().count(),
    }   
    return render(request, 'home.html', context)

@login_required
def joblisting(request):
    jobs = PostJob.objects.all().order_by('-created_at')

    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    job_type = request.GET.get('job_type', '')

    if search:
        jobs = jobs.filter(
            Q(job_title__icontains=search) |
            Q(company_name__icontains=search) |
            Q(job_description__icontains=search)
        )

    
    if category and category != 'All':
        jobs = jobs.filter(category=category)
    
    
    if job_type and job_type != 'All':
        jobs = jobs.filter(job_type=job_type)

    context = {
        'all_jobs': jobs,
        'job_count': jobs.count(),
        'search': search,
        'category': category,
        'job_type': job_type,
    }
    return render(request, 'job_listing.html', context)

def aboutpage(request):
    if request.method == "POST":
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if not name or not email or not message:
            messages.error(request, 'All fields are required.')
            return render(request, 'about.html') 

        if len(message) < 10:
            messages.error(request, 'Message is too short.')
            return render(request, 'about.html')

        if '@' not in email:
            messages.error(request, 'Enter a valid email address.')
            return render(request, 'about.html')

        ContactMessages.objects.create(
            name=name,
            email=email,
            message=message)

        messages.success(request, 'Message sent successfully!')
        return redirect('about')
    else:
        return render(request, 'about.html')

def jobdetail(request, id):
    job = get_object_or_404(PostJob, id=id)
    similar_jobs = PostJob.objects.filter(
        category=job.category).exclude(id=id)[:3]
    
    has_applied = False
    if request.user.is_authenticated:
        has_applied = ApplyJob.objects.filter(job=job,applicant=request.user).exists()

    application_count = ApplyJob.objects.filter(job=job).count()
    context = {
        'job': job,
        'similar_jobs': similar_jobs,
        'has_applied': has_applied,
        'application_count': application_count,
    }
    return render(request, 'jobdetail.html', context)