from config import LTTSSConfig
from piper.voice import PiperVoice
import wave
import numpy as np
from pathlib import Path
from typing import Any


class AudioGenerator():
    def __init__(self, model_config : dict[str: Any], config : LTTSSConfig  ):
        model_file_name = model_config["file_name"]
        if model_file_name.endswith(".onnx"):
            self.name = model_file_name[:-5]
        else:
            print(".onnx extension not detected. It will be added automatically.")
            self.name = model_file_name
        self.model = PiperVoice.load(config.models_dir_path / f"{self.name}.onnx")

        if "speaker_id" in model_config.keys():
            self.speaker_id = model_config["speaker_id"]
        else:
            self.speaker_id = None

        self.inter_sentence_pause_wav_path : Path = config.data_dir_path/ f"intersentence_pause_{self.name}.wav"
        self.initial_latency_wav_path : Path = config.data_dir_path/ f"initial_latency_{self.name}.wav"
        self.sample_wav_path : Path = config.data_dir_path/ f"sample_{self.name}.wav"
        self.generate_sample(self.sample_wav_path)
        self.init_wav_params(self.sample_wav_path)
        self.generate_silent_wav(self.inter_sentence_pause_wav_path, 
                                 config.intersentence_pause_duration)
        self.generate_silent_wav(self.initial_latency_wav_path,
                                 config.initial_latency_duration)
        self.intersentence_pause_bytes = self.generate_silence_bytes(config.intersentence_pause_duration)
        self.initial_latency_bytes = self.generate_silence_bytes(config.initial_latency_duration)



    def generate_audio(self, text : str, path : str | Path):
        wav_file = wave.open(str(path), 'w')
        try:
            self.model.synthesize(text, wav_file, speaker_id=self.speaker_id)
        finally:
            wav_file.close()
        return path
    
    def generate_multisentence_audio(self, sentences : list[str], path : str | Path):
        wav_file = wave.open(str(path), 'w')
        try:
            wav_file.setparams(self.wav_params)
            wav_file.writeframes(self.initial_latency_bytes)
            for sentence in sentences:
                self._synthesize_and_append(sentence, wav_file,)
                wav_file.writeframes(self.intersentence_pause_bytes)
        finally:
            wav_file.close()
        return path
    
    def _synthesize_and_append(self, text : str, wav_file : wave.Wave_write):
        audio_bytes_iterable = self.model.synthesize_stream_raw(text, speaker_id=self.speaker_id)
        for audio_bytes in audio_bytes_iterable:
            wav_file.writeframes(audio_bytes)
        return wav_file
    
    def generate_sample(self, path : str | Path):
        self.generate_audio( "Hello.", path)
        return path
    
    def generate_silence(nframes : int):
        return np.zeros(nframes, dtype='h')


    def init_wav_params(self, path : str | Path):
        with wave.open(str(path), 'r') as wf:
            self.wav_params = wf.getparams()
        
    def generate_silence_bytes(self, duration : float):
        nframes = int(self.wav_params.framerate * duration)
        data = np.zeros(nframes, dtype='h')
        return data.tobytes()

    def generate_silent_wav(self, result_path : str | Path, duration : float):
        with wave.open(str(result_path), 'w') as wf:
            wf.setparams(self.wav_params)
            wf.writeframes(self.generate_silence_bytes(duration))