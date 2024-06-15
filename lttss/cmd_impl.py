import socket
import requests
import threading
import time
import sys

from os_api import OSAPI


def start_server(port):
    from tts_server_controller import app
    app.run(port=port, host="localhost")


def run(os_api : OSAPI, port : int): # TODO : Clean this function

    try:
        response = requests.post(f"http://localhost:{port}/ping")
        if response.text == "pong":
            response = requests.post(f"http://localhost:{port}/uname")
            if response.text == "lttss":
                print(f"a lttss server is already running on port {port}.")
                os_api.notify(f"a lttss server is already running on port {port}.")
                return
            else:
                print(f"Port {port} is occupied by some other process.")
                os_api.notify(f"Port {port} is occupied by some other process.")
                return
        else:
            raise Exception("Server did not respond to ping.")
    except requests.exceptions.ConnectionError:
        try:
            server_thread = threading.Thread(target=start_server, args=(port,))
            server_thread.start()

            request_count = 0
            max_request_count = 20
            while request_count < max_request_count:
                if server_thread.is_alive():
                    try:
                        response = requests.post(f"http://localhost:{port}/ping")
                        if response.text != "pong":
                            print("The server isn't responding to pings.")
                        break
                    except requests.exceptions.ConnectionError:
                        time.sleep(.5)
                        request_count += 1
                else:
                    print("The server process died unexpectedly.")
                    break
            if request_count == max_request_count:
                raise Exception("Server did not start.")
            else:
                try:
                    server_thread.join()
                except KeyboardInterrupt: 
                    max_wait = 10
                    count = 0
                    while server_thread.is_alive() and count < max_wait:
                        time.sleep(1)
                        count += 1

                    if server_thread.is_alive():
                        print("Server is taking too long to stop. Shutdown will be forcefull.")
                    
                    sys.exit(0)
                    
        except Exception as e:
            if isinstance(e, socket.gaierror):
                print(f"Port {port} is occupied by some other process.")
                os_api.notify(f"Port {port} is occupied by some other process.")
            else:
                os_api.notify(f"An error occured while starting the server. \nMessage: {e}")
                raise e
        return



def play_selected( os_api : OSAPI, port : int, lang : str):

    data = os_api.read_clipboard_content()

    if len(data) > 2:
        payload = {"text": data}
        requests.post(f"http://localhost:{port}/play_text/{lang}", json=payload)
    else:
        print("No text to play.")
        os_api.notify("No text to play.")

def append_selected(os_api : OSAPI, port : int, lang : str):

    data = os_api.read_clipboard_content()

    if len(data) > 2:
        payload = {"text": data}
        requests.post(f"http://localhost:{port}/append_text/{lang}", json=payload)
    else:
        print("No text to append.")
        os_api.notify("No text to append.")

def export_selected(os_api : OSAPI, port : int, lang : str):
    data = os_api.read_clipboard_content()

    if len(data) > 2:
        payload = {"text": data}
        response = requests.post(f"http://localhost:{port}/export/{lang}", json=payload)
        path = response.text
        print(f"Exported to {path}")
        os_api.notify(f"Exported to {path}")
    else:
        print("No text to export.")
        os_api.notify("No text to export.")

def speedup(os_api : OSAPI, port : int):
    resonse = requests.post(f"http://localhost:{port}/speedup")
    os_api.notify("LTTSS speed x"+ resonse.text)

def speeddown(os_api : OSAPI,port : int):
    resonse = requests.post(f"http://localhost:{port}/speeddown")
    os_api.notify("LTTSS speed x"+ resonse.text)


def toggle_pause(port : int):
    requests.post(f"http://localhost:{port}/toggle_pause")

def back(port : int):
    requests.post(f"http://localhost:{port}/back")

def shutdown(port : int):
    requests.get(f"http://localhost:{port}/shutdown")