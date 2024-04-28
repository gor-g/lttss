import socket
import requests
import pyperclip
from tts_server_config import TTSServerConfig 



def run(config : TTSServerConfig):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        occupied = s.connect_ex(("localhost", config.port)) == 0
    if occupied:
        response = requests.post(f"http://localhost:{config.port}/uname")
        if response.text == "lttss":
            print("an lttss server is already running on this port.")
        else:
            print(f"Port {config.port} is occupied by some other process.")
    else:
        print("Starting the server.")
        import tts_server_controller
        tts_server_controller.app.run(port=config.port, debug=True)


def play(config : TTSServerConfig):
    text = pyperclip.paste()
    print(text)
    response = requests.post(f"http://localhost:{config.port}/play_text", json={"text": text})
    print(response)