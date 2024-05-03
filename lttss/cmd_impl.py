import socket
import requests
import pyperclip
import subprocess

from config import LTTSSConfig 



def run(config : LTTSSConfig):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        occupied = s.connect_ex(("localhost", config.port)) == 0
    if occupied:
        response = requests.post(f"http://localhost:{config.port}/uname")
        if response.text == "lttss":
            print("a lttss server is already running on this port.")
        else:
            print(f"Port {config.port} is occupied by some other process.")
    else:
        import sys
        import os
        print("Starting the server.")
        python = sys.executable
        server_path = os.path.join(os.path.dirname(__file__), "tts_server_controller.py")
        res = subprocess.Popen([python, server_path])
        if res.returncode == 0:
            print("Server started.")


def play_selected(config : LTTSSConfig):

    data = subprocess.check_output(['xclip', '-selection', config.clipboard, '-o']).decode()

    if len(data) > 2:
        payload = {"text": data}
        requests.post(f"http://localhost:{config.port}/play_text", json=payload)
    else:
        print("No text to play.")

def append_selected(config : LTTSSConfig):
    data = subprocess.check_output(['xclip', '-selection', config.clipboard, '-o']).decode()

    if len(data) > 2:
        payload = {"text": data}
        requests.post(f"http://localhost:{config.port}/append_text", json=payload)
    else:
        print("No text to append.")


def speedup(config : LTTSSConfig):
    requests.post(f"http://localhost:{config.port}/speedup")

def speeddown(config : LTTSSConfig):
    requests.post(f"http://localhost:{config.port}/speeddown")

def export_selected(config : LTTSSConfig):
    data = subprocess.check_output(['xclip', '-selection', config.clipboard, '-o']).decode()

    if len(data) > 2:
        payload = {"text": data}
        response = requests.post(f"http://localhost:{config.port}/export", json=payload)
        path = response.text
        pyperclip.copy(path)
        print(f"Exported to {path}")
    else:
        print("No text to export.")

def toggle_pause(config : LTTSSConfig):
    requests.post(f"http://localhost:{config.port}/toggle_pause")

def back(config : LTTSSConfig):
    requests.post(f"http://localhost:{config.port}/back")