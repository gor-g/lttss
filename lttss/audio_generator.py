from piper import AudioChunk, SynthesisConfig
from lttss.services.config import LTTSSConfig
from piper.voice import PiperVoice
import wave
import numpy as np
from pathlib import Path
from typing import Iterable, cast


class AudioGenerator():
    def __init__(self, model_config : dict[str, str|int], config : LTTSSConfig  ):

        self.speaker_id: int | None
        self.name: str
        model_file_name: str = cast(str, model_config["file_name"])
        if model_file_name.endswith(".onnx"):
            self.name = model_file_name[:-5]
        else:
            print(".onnx extension not detected. It will be added automatically.")
            self.name = model_file_name
        self.model = PiperVoice.load(config.models_dir_path / f"{self.name}.onnx")

        if "speaker_id" in model_config.keys():
            self.speaker_id = cast(int, model_config["speaker_id"])
        else:
            self.speaker_id = None


        self.syn_config = SynthesisConfig(speaker_id = self.speaker_id, 
                                            volume=1,  
                                            length_scale=1.0, 
                                            noise_scale=1.0,  
                                            noise_w_scale=1.0,  
                                            normalize_audio=False, 
        )

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
            self.model.synthesize_wav(text, wav_file, 
                                  syn_config = self.syn_config)
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
        chunks:Iterable[AudioChunk] = self.model.synthesize(text, self.syn_config)
        for chunk in chunks:
            wav_file.writeframes(chunk.audio_int16_bytes)
        return wav_file
    
    def generate_sample(self, path : str | Path):
        self.generate_audio( "Hello.", path)
        return path

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