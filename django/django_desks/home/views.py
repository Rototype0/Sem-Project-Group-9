from django.shortcuts import render, get_object_or_404, redirect

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

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

def save_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        profile_name = data.get('profileName')
        profile_height = data.get('profileHeight')

        # Save logic here
        message = f"Height profile '{profile_name}' with height {profile_height} cm saved."
        return JsonResponse({'message': message}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def apply_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        profile_name = data.get('profileName')
        profile_height = data.get('profileHeight')

        # Logic to apply the profile
        # For example, send a command to the moving table system
        message = f"Height profile '{profile_name}' with height {profile_height} cm applied."
        return JsonResponse({'message': message}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)