from django.shortcuts import render
from user_authentication.models import DeskUserProfile, User
from desk_controller.views import desk_state_update

# Create your views here.

def dashboard(request):
    if request.user.is_authenticated:
        current_user = DeskUserProfile.objects.get(user=User.objects.get(id=request.user.id))
        context ={
            'height1': current_user.height1_cm,
            'height2': current_user.height2_cm,
            'height3': current_user.height3_cm,
            'height4': current_user.height4_cm,
            'height5': current_user.height5_cm,
            'height6': current_user.height6_cm,
            'name1': current_user.height1_name,
            'name2': current_user.height2_name,
            'name3': current_user.height3_name,
            'name4': current_user.height4_name,
            'name5': current_user.height5_name,
            'name6': current_user.height6_name,
        }

        current_desk_id = "cd:fb:1a:53:fb:e6"

        if request.method == "POST":
            name = request.POST.get('name')
            print(name)
            match name:
                case 'set_height1':
                    desk_state_update(current_desk_id, current_user.height1_cm * 10)
                    print("Set current height to:" + str(current_user.height1_cm))
                case 'set_height2':
                    desk_state_update(current_desk_id, current_user.height2_cm * 10)
                    print("Set current height to:" + str(current_user.height2_cm))
                case 'set_height3':
                    desk_state_update(current_desk_id, current_user.height3_cm * 10)
                    print("Set current height to:" + str(current_user.height3_cm))
                case 'set_height4':
                    desk_state_update(current_desk_id, current_user.height4_cm * 10)
                    print("Set current height to:" + str(current_user.height4_cm))
                case 'set_height5':
                    desk_state_update(current_desk_id, current_user.height5_cm * 10)
                    print("Set current height to:" + str(current_user.height5_cm))
                case 'set_height6':
                    desk_state_update(current_desk_id, current_user.height6_cm * 10)
                    print("Set current height to:" + str(current_user.height6_cm))
                case _:
                    print("no name found")

        return render(request, 'home/dashboard.html', context)
    else:
        messages.error(request, ("User not authenticated"))
        return redirect('about')

def about(request):
    return render(request, 'home/about.html')
