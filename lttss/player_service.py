
import os
from time import sleep
import subprocess
import atexit
import json
import socket

class PlayerService:
    def run(self): raise NotImplementedError("This is a placeholder method, call a child class instead.")
    def append(self, path): raise NotImplementedError("This is a placeholder method, call a child class instead.")
    def load_new_sequance_tip(self, path): raise NotImplementedError("This is a placeholder method, call a child class instead.")
    def set_speed(self, speed): raise NotImplementedError("This is a placeholder method, call a child class instead.")
    def terminate(self): raise NotImplementedError("This is a placeholder method, call a child class instead.")
    def toggle_pause(self): raise NotImplementedError("This is a placeholder method, call a child class instead.")
    def back(self): raise NotImplementedError("This is a placeholder method, call a child class instead.")




class MPV(PlayerService):
    def __init__(self, input_ipc_server, speed=2) -> None:
        self.input_ipc_server = input_ipc_server
        self.speed = speed
        
    def run(self):
        self.process = subprocess.Popen(f"mpv --no-terminal --no-video --idle --input-ipc-server={self.input_ipc_server}", shell=True, )
        sleep(2)
        self.set_speed(self.speed)
        print("MPV running...")
        atexit.register(self.terminate)
        return
    
    def sleep(self):
        sleep(0.1)
    
    def send_command(self, command):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(str(self.input_ipc_server))
            s.sendall((json.dumps(command) + '\n').encode('utf-8'))
        self.sleep()

    def append(self, path):
        command = {"command": ["loadfile", str(path), "append-play"]}
        self.send_command(command)

    def load_new_sequance_tip(self, path):
        command = {"command": ["loadfile", str(path), "replace"]}
        self.send_command(command)
        command = {"command": ["playlist-clear"]}
        self.send_command(command)

    def set_speed(self, speed):
        self.speed = speed
        command = {"command": ["set_property", "speed", self.speed]}
        self.send_command(command)

    def terminate(self):
        self.send_command({"command": ["quit"]})
        self.process.terminate()
        return
    
    def toggle_pause(self):
        self.send_command({"command": ["cycle", "pause"]})
        return

    def back(self):
        self.send_command({"command": ["playlist-prev"]})
        return
    

if __name__=="__main__":
    mpv = MPV('/tmp/mpvsocket2')
    mpv.run()
    sleep(1)

    mpv.append('/home/storage/trash/piper_toplay.wav')
    sleep(5)

    mpv.append('/home/storage/trash/piper_toplay.wav')
    sleep(5)

    mpv.load_new_sequance_tip('/home/storage/trash/piper_toplay.wav')

    mpv.clear()