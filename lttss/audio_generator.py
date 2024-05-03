from config import LTTSSConfig
from piper.voice import PiperVoice
import wave
import numpy as np
from pathlib import Path


class AudioGenerator():
    def __init__(self, model_file_name : str, config : LTTSSConfig  ):
        if model_file_name.endswith(".onnx"):
            self.name = model_file_name[:-5]
        else:
            print(".onnx extension not detected. It will be added automatically.")
            self.name = model_file_name
        self.model = PiperVoice.load(config.models_dir_path / f"{self.name}.onnx")

        self.inter_sentence_pause_wav_path = config.data_dir_path/ f"intersentence_pause_{self.name}.wav"
        self.initial_latency_wav_path = config.data_dir_path/ f"initial_latency_{self.name}.wav"
        self.sample_wav_path = config.data_dir_path/ f"sample_{self.name}.wav"
        self.generate_sample(self.sample_wav_path)
        self.generate_silent_wav(self.inter_sentence_pause_wav_path, 
                                 config.intersentence_pause_duration)
        self.generate_silent_wav(self.initial_latency_wav_path,
                                 config.initial_latency_duration)


    def generate_audio(self, text, path):
        wav_file = wave.open(str(path), 'w')
        try:
            self.model.synthesize(text, wav_file)
        finally:
            wav_file.close()
        return path

    def generate_sample(self, path):
        self.generate_audio( "Hello.", path)
        return self.sample_wav_path
    
    def generate_silent_wav(self, result_path, duration):
        # Open the sample file to get the parameters
        with wave.open(str(self.sample_wav_path), 'r') as wf:
            params = wf.getparams()

        # Generate the silent data
        nframes = int(params.framerate * duration)
        data = np.zeros(nframes, dtype='h')

        # Open the target file and write the data with the copied parameters
        with wave.open(str(result_path), 'w') as wf:
            wf.setparams(params)
            wf.writeframes(data.tobytes())