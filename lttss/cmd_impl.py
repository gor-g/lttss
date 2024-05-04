import socket
import requests
import pyperclip
import subprocess

from config import LTTSSConfig 

from os_api import OSAPI



def run(port : int):
    try:
        from tts_server_controller import app
        app.run(port=port , host="localhost")
    except Exception as e:
        if isinstance(e, socket.gaierror):
            response = requests.post(f"http://localhost:{port}/uname")
            if response.text == "lttss":
                print("a lttss server is already running on this port.")
            else:
                print(f"Port {port} is occupied by some other process.")
        else:
            raise e
    


def play_selected( os_api : OSAPI, port : int, lang : str):

    data = os_api.read_clipboard_content()

    if len(data) > 2:
        payload = {"text": data}
        requests.post(f"http://localhost:{port}/play_text/{lang}", json=payload)
    else:
        print("No text to play.")

def append_selected(os_api : OSAPI, port : int, lang : str):

    data = os_api.read_clipboard_content()

    if len(data) > 2:
        payload = {"text": data}
        requests.post(f"http://localhost:{port}/append_text/{lang}", json=payload)
    else:
        print("No text to append.")

def export_selected(os_api : OSAPI, port : int, lang : str):
    data = os_api.read_clipboard_content()

    if len(data) > 2:
        payload = {"text": data}
        response = requests.post(f"http://localhost:{port}/export/{lang}", json=payload)
        path = response.text
        print(f"Exported to {path}")
    else:
        print("No text to export.")

def speedup(port : int):
    requests.post(f"http://localhost:{port}/speedup")

def speeddown(port : int):
    requests.post(f"http://localhost:{port}/speeddown")


def toggle_pause(port : int):
    requests.post(f"http://localhost:{port}/toggle_pause")

def back(port : int):
    requests.post(f"http://localhost:{port}/back")