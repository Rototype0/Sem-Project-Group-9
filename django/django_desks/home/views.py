from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseForbidden

from .models import UserProfile

# Create your views here.

def dashboard(request):
    return render(request, 'home/dashboard.html')

def about(request):
    return render(request, 'home/about.html')

def dasboard(request):

    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.role == 'manager':
        return render(request, 'dashboard/manager_dashboard.html')
    elif user_profile.role == 'user':
        return render(request, 'dashboard/user_dashboard.html')
    elif user_profile.role == 'cleaner':
        return render(request, 'dashboard/cleaner_dashboard.html')
    else:
        return HttpResponseForbidden("Access Denied")
