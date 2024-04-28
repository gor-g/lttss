import platform
import array
import numpy as np
import wave
import struct

def get_os():
    os_name = platform.system()
    if os_name == 'Windows':
        return 'Windows'
    elif os_name == 'Linux':
        return 'Linux'
    elif os_name == 'Darwin':
        return 'macOS'
    else:
        return 'Unknown OS'


def generate_silent_wav(path, duration=0.2, framerate=44100):
    nframes = int(framerate * duration)

    data = array.array('h', [0] * nframes)

    with wave.open(str(path), 'w') as wf:
        wf.setnchannels(1)  # mono
        wf.setsampwidth(2)  # 2 bytes = 16 bits
        wf.setframerate(framerate)

        wf.writeframes(data.tobytes())

import wave

def generate_silent_wav(sample_path, result_path, duration=0.2):
    # Open the source file and read the parameters
    with wave.open(str(sample_path), 'r') as wf:
        params = wf.getparams()

    # Generate the silent data
    nframes = int(params.framerate * duration)
    data = array.array('h', [0] * nframes)

    # Open the target file and write the data with the copied parameters
    with wave.open(str(result_path), 'w') as wf:
        wf.setparams(params)
        wf.writeframes(data.tobytes())



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

generate_sinusoidal_wav('sinusoidal.wav', 1.0, 440.0, 44100)