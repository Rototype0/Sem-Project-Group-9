from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required

def profile(request):
    context = {'user': request.user}
    return render(request, 'authenticate/profile.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
            
        else:
            messages.success(request, ("There was an error logging in, try again."))
            return redirect('login')        
            
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    #messages.success(request, ("You were Logged Out"))
    return redirect('about')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = form.cleaned_data['role'] 
            user.save() 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password) 
            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect('dashboard') 
    else:
        form = RegisterUserForm()

    context = {'form':form,}
    return render(request, 'authenticate/register_user.html', context)


@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}

    if user.user_type == 'manager':
        return render(request, 'manager_dashboard.html', context)
    elif user.user_type == 'cleaner':
        return render(request, 'cleaner_dashboard.html', context)
    else:
        return render(request, 'member_dashboard.html', context)