import argparse
import socket
import tts_server_config
import requests
import pyperclip

parser = argparse.ArgumentParser(description='TTS Command')

# Add arguments
parser.add_argument('-r', '--run', action='store_true', help='Run the server.', default=False)
parser.add_argument('-p', '--play', action='store_true', help='Generate and play the sound.', default=False)
parser.add_argument('-ap', '--append-to-play', action='store_true', help='Append the text at the end of the generated sound.', default=False)
parser.add_argument('-s', '--speed-up', action='store_true', help='Speed up the sound.', default=False)
parser.add_argument('-d', '--speed-down', action='store_true', help='Speed down the sound.', default=False)
parser.add_argument('-e', '--export', action='store_true', help='Export the sound.', default=False)

# Parse the arguments
args = parser.parse_args()

config = tts_server_config.TTSServerConfig()

if args.run:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        occupied = s.connect_ex(("localhost", config.port)) == 0
    if occupied:
        response = requests.post(f"http://localhost:{config.port}/uname")
        if response.text == "lttss":
            print("an lttss server is already running on this port.")
        else:
            print(f"Port {config.port} is already by some other process.")
    else:
        print("Starting the server.")
        import tts_server_controller
        tts_server_controller.app.run(port=config.port, debug=True)

elif args.play:
    text = pyperclip.paste()
    response = requests.post(f"http://localhost:{config.port}/play_text", json={"text": text})
    print(response)