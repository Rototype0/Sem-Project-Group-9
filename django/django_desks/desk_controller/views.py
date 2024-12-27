from django.shortcuts import render
import requests, json, asyncio
from django.http import JsonResponse
from .models import Desk

def fetch_desks(request):
    api_base_url = "http://localhost:8000/api/v2/"
    
    api_key = "E9Y2LxT4g1hQZ7aD8nR3mWx5P0qK6pV7"
    
    api_url = f"{api_base_url}{api_key}/desks"

    response = requests.get(api_url)
    response.raise_for_status()

    desks = response.json()

    desk_dict = {f"desk_{i+1}": desk for i, desk in enumerate(desks)}
    
    return JsonResponse(desk_dict, safe=False)


def desk_info(request, desk_id):
    api_base_url = "http://localhost:8000/api/v2/"
    api_key = "E9Y2LxT4g1hQZ7aD8nR3mWx5P0qK6pV7"
    api_url = f"{api_base_url}{api_key}/desks/"

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
        desk.save()

        return JsonResponse({f"desk_{desk_id}": desk_details})

    else:
        return JsonResponse({'error': 'Desk not found or invalid desk_id'}, status=404)
    
def desk_state_update(request, desk_id):

    api_base_url = "http://localhost:8000/api/v2/"
    api_key = "E9Y2LxT4g1hQZ7aD8nR3mWx5P0qK6pV7"
    api_url = f"{api_base_url}{api_key}/desks/"

    response = requests.get(api_url)
    response.raise_for_status()
    desks = response.json()

    mac_address = desks[desk_id - 1]

    api_url_2 = f"{api_base_url}{api_key}/desks/{mac_address}/state/"

    state = '{"position_mm": 1000}'

    requests.put(api_url_2, state)
    response = requests.get(api_url_2)
    response.raise_for_status()
    updated_data = response.json()

    return JsonResponse({f"desk_{desk_id}_state": updated_data})

import requests
from django.http import JsonResponse

def update_all_desk_states(request, desk_id):
    api_base_url = "http://localhost:8000/api/v2/"
    api_key = "E9Y2LxT4g1hQZ7aD8nR3mWx5P0qK6pV7"
    api_url = f"{api_base_url}{api_key}/desks/"

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
