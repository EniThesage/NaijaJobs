from django.shortcuts import render, redirect, resolve_url
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


# Create your views here.
class SignUpView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if not firstname or not lastname or not username or not email or not password or not password2:
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'signup.html')
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')
        if '@' not in email or '.' not in email:
            messages.error(request, 'Enter a valid email address.')
            return render(request, 'signup.html')
        username = username.lower()
        email = email.lower()
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Choose another or login.')
            return render(request, 'signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'signup.html')
        user = User.objects.create_user(first_name=firstname,
                                    last_name=lastname,
                                    username=username,
                                    email=email,
                                    password=password)
        login (request, user)
        messages.success(request, f'Welcome to NaijaJobs, {firstname}!')
        return redirect(resolve_url('home'))

def loginview(request):
    if request.method == 'POST':
        next_page = request.GET.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'All feilds are required.')
            return render(request, 'login.html')
        username = username.lower()
        username_exists = User.objects.filter(username=username).first()
        if not username_exists:
            messages.error(request, 'invalid login credentials.')
            return render(request, 'login.html')
        user = authenticate(username=username, password=password)
        if not user:
            messages.error(request, 'invalid login credentials.')
            return render(request, 'login.html')
    
        login (request, user)
        messages.success(request, 'login successful')
        return redirect(next_page or resolve_url('home'))
    else:
        return render(request, 'login.html')


def logoutview(request):
    logout(request)
    messages.success(request, 'logged out successfully')
    return redirect('login')
        

def error_404(request, exception):
    return render(request, 'error_404.html')
    

def error_500(request):
    return render(request, 'error_500.html')