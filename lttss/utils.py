import platform
import numpy as np
import wave
from os_api import OSAPI, LinuxAPI, WindowsAPI, MacOSAPI

def get_os_api()-> OSAPI:
    os_name = platform.system()
    if os_name == 'Windows':
        return WindowsAPI()
    elif os_name == 'Linux':
        return LinuxAPI()
    elif os_name == 'Darwin':
        return MacOSAPI()
    else:
        raise Exception(f"Unsupported OS: {os_name}")



def generate_sinusoidal_wav(path, duration=1.0, frequency=440.0, framerate=44100):
    # Generate the time values
    t = np.linspace(0, duration, int(framerate * duration), False)

    # Generate the audio signal
    signal = 0.5 * np.sin(frequency * 2 * np.pi * t)

    # Convert to 16-bit data
    signal = (signal * 32767).astype(np.int16)

    # Write the data to a .wav file
    with wave.open(str(path), 'w') as wf:
        wf.setnchannels(1)  # mono
        wf.setsampwidth(2)  # 2 bytes = 16 bits
        wf.setframerate(framerate)
        wf.writeframes(signal.tobytes())

if __name__ == "__main__":
    generate_sinusoidal_wav('sinusoidal.wav', 1.0, 440.0, 44100)