from django.shortcuts import render
import requests, json
from django.http import JsonResponse
from .models import Desk
import socket
import time
import struct

def fetch_desks(request):
    api_base_url = "http://localhost:50/api/v2/"
    
    api_key = "E9Y2LxT4g1hQZ7aD8nR3mWx5P0qK6pV7"
    
    api_url = f"{api_base_url}{api_key}/desks"

    response = requests.get(api_url)
    response.raise_for_status()

    desks = response.json()

    desk_dict = {f"desk_{i+1}": desk for i, desk in enumerate(desks)}
    
    return JsonResponse(desk_dict, safe=False)


def desk_info(request, desk_id):
    api_base_url = "http://localhost:50/api/v2/"
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


def connect_to_pico(server_host_ip):
    server_port = 4242      # Use the port number the server is listening on
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((server_host_ip, server_port))
    print(f"Connected to server {server_host_ip}:{server_port}")
    client_socket.send(b'\x01')
    for i in range(10):
        msg = client_socket.recv(28)
        btn_state, pressed, pressed_since_last, potentiometer, light_intensity, temp, humidity = struct.unpack("<BxxxIIffff", msg)
        print(btn_state, pressed, pressed_since_last, potentiometer, light_intensity, temp, humidity)
        if i % 6 == 0:
            client_socket.send(b'\x05')
    client_socket.send(b'\x02')
    time.sleep(2)
    client_socket.close()

def desk_state_update(request, desk_id):

    api_base_url = "http://localhost:50/api/v2/"
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

