import socket
import requests
import pyperclip
import requests
import subprocess

from tts_server_config import TTSServerConfig 



def run(config : TTSServerConfig):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        occupied = s.connect_ex(("localhost", config.port)) == 0
    if occupied:
        response = requests.post(f"http://localhost:{config.port}/uname")
        if response.text == "lttss":
            print("a lttss server is already running on this port.")
        else:
            print(f"Port {config.port} is occupied by some other process.")
    else:
        print("Starting the server.")
        import tts_server_controller
        tts_server_controller.app.run(port=config.port, debug=True)


def play_selected(config : TTSServerConfig):

    data = subprocess.check_output(['xclip', '-selection', config.clipboard, '-o']).decode()

    if len(data) > 2:
        payload = {"text": data}
        requests.post(f"http://localhost:{config.port}/play_text", json=payload)
    else:
        print("No text to play.")

def append_selected(config : TTSServerConfig):
    data = subprocess.check_output(['xclip', '-selection', config.clipboard, '-o']).decode()

    if len(data) > 2:
        payload = {"text": data}
        requests.post(f"http://localhost:{config.port}/append_text", json=payload)
    else:
        print("No text to append.")


def speedup(config : TTSServerConfig):
    requests.post(f"http://localhost:{config.port}/speedup")

def speeddown(config : TTSServerConfig):
    requests.post(f"http://localhost:{config.port}/speeddown")

def export_selected(config : TTSServerConfig):
    data = subprocess.check_output(['xclip', '-selection', config.clipboard, '-o']).decode()

    if len(data) > 2:
        payload = {"text": data}
        response = requests.post(f"http://localhost:{config.port}/export", json=payload)
        path = response.text
        pyperclip.copy(path)
        print(f"Exported to {path}")
    else:
        print("No text to export.")

def toggle_pause(config : TTSServerConfig):
    requests.post(f"http://localhost:{config.port}/toggle_pause")