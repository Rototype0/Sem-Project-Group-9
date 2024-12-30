from django.shortcuts import render
from user_authentication.models import DeskUserProfile, User
from desk_controller.views import desk_state_update, fetch_desks

# Create your views here.

def select_desk(request):
    if request.user.is_authenticated:
        desks_active = fetch_desks()
        if request.method == "POST":
            a = request.POST['desk_drop_menu']
            print(a)
        return render(request, 'home/desk_selection.html', {'desks': desks_active})
    else:
        messages.error(request, ("User not authenticated"))
        return redirect('about')

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

        if request.method == "POST":
            name = request.POST.get('name')
            print(name)
            match name:
                case 'set_current_desk':
                    current_user.current_selected_desk_mac_address = request.POST.get('desk_drop_menu')
                    print(current_user.current_selected_desk_mac_address)
                    current_user.save()
                case 'set_height1':
                    print(current_user.current_selected_desk_mac_address)
                    desk_state_update(current_user.current_selected_desk_mac_address, current_user.height1_cm * 10)
                    print("Set current height to:" + str(current_user.height1_cm))
                case 'set_height2':
                    desk_state_update(current_user.current_selected_desk_mac_address, current_user.height2_cm * 10)
                    print("Set current height to:" + str(current_user.height2_cm))
                case 'set_height3':
                    desk_state_update(current_user.current_selected_desk_mac_address, current_user.height3_cm * 10)
                    print("Set current height to:" + str(current_user.height3_cm))
                case 'set_height4':
                    desk_state_update(current_user.current_selected_desk_mac_address, current_user.height4_cm * 10)
                    print("Set current height to:" + str(current_user.height4_cm))
                case 'set_height5':
                    desk_state_update(current_user.current_selected_desk_mac_address, current_user.height5_cm * 10)
                    print("Set current height to:" + str(current_user.height5_cm))
                case 'set_height6':
                    desk_state_update(current_user.current_selected_desk_mac_address, current_user.height6_cm * 10)
                    print("Set current height to:" + str(current_user.height6_cm))
                case _:
                    print("no name found")

        return render(request, 'home/dashboard.html', context)
    else:
        messages.error(request, ("User not authenticated"))
        return redirect('about')

def about(request):
    return render(request, 'home/about.html')
