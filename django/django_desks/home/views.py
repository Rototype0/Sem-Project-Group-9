from django.shortcuts import render, get_object_or_404, redirect

from .models import Desk, HeightProfile

# Create your views here.

def dashboard(request):
    return render(request, 'home/dashboard.html')

def charts(request):
    return render(request, 'home/charts.html')

def modes(request):
    return render(request, 'home/modes.html')

def profile(request):
    return render(request, 'home/profile.html')

def applyHeightProfile(request, desk_id, profile_id):
    desk = get_object_or_404(Desk, id = desk_id)
    profile = get_object_or_404(HeightProfile, id = profile_id)
    desk.height = profile.height
    desk.save()
    return render('home/dashboard.html', {'profile': profile})