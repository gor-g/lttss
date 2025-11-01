
from time import sleep
import subprocess
import atexit
import json
import socket
from typing import Any
from pathlib import Path
from abc import ABC, abstractmethod

class PlayerService(ABC):
    @abstractmethod
    def run(self): pass
    @abstractmethod
    def append(self, path : Path | str): pass
    @abstractmethod
    def load_new_sequance_tip(self, path : Path | str): pass
    @abstractmethod
    def set_speed(self, speed : float): pass
    @abstractmethod
    def terminate(self): pass
    @abstractmethod
    def toggle_pause(self): pass
    @abstractmethod
    def back(self): pass
    @abstractmethod
    def speedup(self)->float: pass
    @abstractmethod
    def speeddown(self)->float: pass



class MPV(PlayerService):
    def __init__(self, input_ipc_server: str, speed: int =2, speed_increment: float = .1) -> None:
        self.input_ipc_server = input_ipc_server
        self.speed = speed
        self.speed_increment = speed_increment
        
    def run(self):
        self.process = subprocess.Popen(f"mpv --no-terminal --no-video --idle --input-ipc-server={self.input_ipc_server}", shell=True, )
        sleep(2)
        self.set_speed(self.speed)
        print("MPV running...")
        atexit.register(self.terminate)
        return
    
    def sleep(self):
        sleep(0.1)
    
    def send_command(self, command : dict[str,list[Any]]):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(str(self.input_ipc_server))
            s.sendall((json.dumps(command) + '\n').encode('utf-8'))
        self.sleep()

    def append(self, path : Path | str):
        command = {"command": ["loadfile", str(path), "append-play"]}
        self.send_command(command)

    def load_new_sequance_tip(self, path : Path | str):
        command = {"command": ["loadfile", str(path), "replace"]}
        self.send_command(command)
        command = {"command": ["playlist-clear"]}
        self.send_command(command)

    def set_speed(self, speed : float):
        self.speed = speed
        command: dict[str,list[str|float]] = {"command": ["set_property", "speed", self.speed]}
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
    
    def speedup(self):
        self.speed = self.speed + self.speed_increment
        return self.speed

    def speeddown(self):
        self.speed = self.speed - self.speed_increment
        return self.speed
    

if __name__=="__main__":
    mpv = MPV('/tmp/mpvsocket2')
    mpv.run()
    sleep(1)

    mpv.append('/home/storage/trash/piper_toplay.wav')
    sleep(5)

    mpv.append('/home/storage/trash/piper_toplay.wav')
    sleep(5)

    mpv.load_new_sequance_tip('/home/storage/trash/piper_toplay.wav')
