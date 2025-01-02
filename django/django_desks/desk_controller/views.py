from django.shortcuts import render
import requests, json
from django.http import JsonResponse
from .models import Desk
import socket
import time
import struct

def fetch_desks():
    api_base_url = "http://localhost:50/api/v2/"
    
    api_key = "E9Y2LxT4g1hQZ7aD8nR3mWx5P0qK6pV7"
    
    api_url = f"{api_base_url}{api_key}/desks"

    response = requests.get(api_url)
    response.raise_for_status()

    desks = response.json()

    desk_dict = {f"desk_{i+1}": desk for i, desk in enumerate(desks)}
    
    return desk_dict
    #return JsonResponse(desk_dict, safe=False)


def desk_info(request, mac_address):
    if request.method == "GET":
        api_base_url = "http://localhost:50/api/v2/"
        api_key = "E9Y2LxT4g1hQZ7aD8nR3mWx5P0qK6pV7"
        api_url = f"{api_base_url}{api_key}/desks/{mac_address}/state"

        response = requests.get(api_url)
        response.raise_for_status()
        desk_details = response.json()

        return JsonResponse(desk_details)


'''def connect_to_pico(server_host_ip):
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
    client_socket.close()'''

def desk_state_update(mac_address, position_mm):
    api_base_url = "http://localhost:50/api/v2/"
    api_key = "E9Y2LxT4g1hQZ7aD8nR3mWx5P0qK6pV7"

    api_url = f"{api_base_url}{api_key}/desks/{mac_address}/state/"
    
    state = {"position_mm": int(position_mm)}
    response = requests.put(api_url, json=state)
    #response.raise_for_status()


