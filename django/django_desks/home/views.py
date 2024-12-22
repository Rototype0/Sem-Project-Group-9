from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, 'home/dashboard.html')

def about(request):
    return render(request, 'home/about.html')
