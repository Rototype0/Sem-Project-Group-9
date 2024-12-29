from django.shortcuts import render
import requests, json, asyncio
from requests.exceptions import ConnectionError, Timeout, RequestException
from django.http import JsonResponse
from .models import Desk

def fetch_desks(request):
    api_base_url = "http://localhost:8000/api/v2/"
    api_key = "E9Y2LxT4g1hQZ7aD8nR3mWx5P0qK6pV7"
    api_url = f"{api_base_url}{api_key}/desks"

    try:
        response = requests.get(api_url, timeout=10)  # Add a timeout
        response.raise_for_status()  # Raise HTTP errors if any

        desks = response.json()
        desk_dict = {f"desk_{i+1}": desk for i, desk in enumerate(desks)}
        return JsonResponse(desk_dict, safe=False)

    except ConnectionError:
        return JsonResponse({"error": "Unable to connect to the API server. Please try again later."}, status=404)
    except Timeout:
        return JsonResponse({"error": "The request to the API server timed out. Please try again later."}, status=504)
    except RequestException as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)



def desk_info(request, desk_id):
    api_base_url = "http://localhost:8000/api/v2/"
    api_key = "E9Y2LxT4g1hQZ7aD8nR3mWx5P0qK6pV7"
    api_url = f"{api_base_url}{api_key}/desks/"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        desks = response.json()

        if isinstance(desks, list) and 1 <= desk_id <= len(desks):
            mac_address = desks[desk_id - 1]

            second_api_url = f"{api_base_url}{api_key}/desks/{mac_address}/"

            second_response = requests.get(second_api_url)
            second_response.raise_for_status()
            desk_details = second_response.json()

            desk, created = Desk.objects.get_or_create(mac_address=mac_address,)
            desk.name = desk_details.get('config', {}).get('name', 'Unknown')
            desk.state = desk_details.get('state', {}).get('position_mm', 'Unknown')
            desk.status = desk_details.get('state', {}).get('status', 'Unknown')
            desk.save()

            return JsonResponse({f"desk_{desk_id}": desk_details})

        else:
            return JsonResponse({'error': 'Desk not found or invalid desk_id'}, status=404)
    except ConnectionError:
        return JsonResponse({"error": "Unable to connect to the API server. Please try again later."}, status=404)
    except RequestException as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    
def desk_state_update(request, desk_id):
    api_base_url = "http://localhost:8000/api/v2/"
    api_key = "E9Y2LxT4g1hQZ7aD8nR3mWx5P0qK6pV7"
    api_url = f"{api_base_url}{api_key}/desks/"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        desks = response.json()

        mac_address = desks[desk_id - 1]

        api_url_2 = f"{api_base_url}{api_key}/desks/{mac_address}/state/"

        position_mm = request.POST.get("position_mm", 1000)
        
        state = {"position_mm": int(position_mm)}
        response = requests.put(api_url_2, json=state)
        response.raise_for_status()

        updated_response = requests.get(api_url_2)
        updated_response.raise_for_status()
        updated_data = updated_response.json()

        return render(request, "desk_controller/desk_state_update.html", {
                "success": f"Desk {desk_id} state updated successfully!",
                "updated_data": updated_data,
                })
    except ConnectionError:
            return render(request, "desk_controller/desk_state_update.html", {"error": "Unable to connect to the API server. Please try again later."})
    except RequestException as e:
            return render(request, "desk_controller/desk_state_update.html", {"error": f"An error occurred: {str(e)}"})

def update_all_desk_states(request, desk_id):
    api_base_url = "http://localhost:8000/api/v2/"
    api_key = "E9Y2LxT4g1hQZ7aD8nR3mWx5P0qK6pV7"
    api_url = f"{api_base_url}{api_key}/desks/"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        desks = response.json()

        results = {} 
        state = '{"position_mm": 1000}' 

        for desk_id, mac_address in enumerate(desks, start=1):
            try:
                
                api_url_state = f"{api_base_url}{api_key}/desks/{mac_address}/state/"
                put_response = requests.put(api_url_state, data=state)
                put_response.raise_for_status()

                get_response = requests.get(api_url_state)
                get_response.raise_for_status()
                updated_data = get_response.json()

                results[f"desk_{desk_id}_state"] = updated_data
            except Exception as e:
                results[f"desk_{desk_id}_error"] = str(e)

        return JsonResponse({"results": results})
    except ConnectionError:
        return JsonResponse({"error": "Unable to connect to the API server. Please try again later."}, status=404)
    except RequestException as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)