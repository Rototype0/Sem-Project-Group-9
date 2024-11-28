from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, 'home/dashboard.html')

def charts(request):
    return render(request, 'home/charts.html')

def modes(request):
    return render(request, 'home/modes.html')

def profile(request):
    return render(request, 'home/profile.html')