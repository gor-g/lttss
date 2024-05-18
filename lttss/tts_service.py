import os
from config import LTTSSConfig
import time
from langdetect import detect
from player_service import PlayerService, MPV
from text_processor import TextProcessor
from pathlib import Path

from audio_generator import AudioGenerator

class TTSService():
    def __init__(self, config : LTTSSConfig):
        self.config : LTTSSConfig = config
        self.init_dirs()
        self.load_models()
        self.load_text_processors()
        self.player : PlayerService  = MPV(self.config.mpv_socket_dir_path, self.config.default_speed)
        self.player.run()
        self.play_text("LTTSS is running!", "english")
    
    def init_dirs(self):
        os.makedirs(self.config.tmp_dir_path, exist_ok=True)
        os.makedirs(self.config.export_dir_path, exist_ok=True)
        os.makedirs(self.config.to_play_dir_path, exist_ok=True)

    def load_models(self):
        self.generators : dict[str : AudioGenerator] = dict()
        for lang, model_file_name in self.config.models.items():
            self.generators[lang] = AudioGenerator( model_file_name, self.config)
        self.generators['fallback'] = self.generators[self.config.fallback_lang]

    def load_text_processors(self):
        self.text_processors : dict[str : TextProcessor] = dict()
        for lang in self.config.models.keys():
            self.text_processors[lang] = TextProcessor(lang)
        self.text_processors['fallback'] = self.text_processors[self.config.fallback_lang]

    def make_tmp_wav_path(self):
        return f"{self.config.to_play_dir_path}/voice-{time.time_ns()}.wav"
    
    def make_export_wav_path(self):
        return f"{self.config.export_dir_path}/voice-{time.time_ns()}.wav"
    
    def generate_audio(self, lang : str, text : str, path : str | Path):
        path = self.generators[lang].generate_audio(text, path)
        return path
    
    def read_from_file(self, textfilename : str):
        with open(textfilename, 'r') as f:
            text = f.read()
        return text
    
    def play_sentences(self, sentences : list[str], lang : str):
        sentence = sentences.pop(0)
        path = self.make_tmp_wav_path()
        self.generate_audio(lang, sentence, path)
        self.player.load_new_sequance_tip(self.config.intersentence_silence_wav_path)
        self.player.append(path)
        for sentence in sentences:
            path = self.make_tmp_wav_path()
            self.generate_audio(lang, sentence, path)
            self.player.append(self.config.intersentence_silence_wav_path)
            self.player.append(path)
        return

    def append_sentences(self, sentences, lang):
        for sentence in sentences:
            path = self.make_tmp_wav_path()
            self.generate_audio(lang, sentence, path)
            self.player.append(self.config.intersentence_silence_wav_path)
            self.player.append(path)
        return
    
    def play_text(self, text, lang):
        sentences = self.text_processors[lang].process(text)
        self.play_sentences(sentences, lang)

    def append_text(self, text, lang):
        sentences = self.text_processors[lang].process(text)
        self.append_sentences(sentences, lang)

    def export_text(self, text, lang):
        path = self.make_export_wav_path()
        self.generate_audio(lang, text, path)
        return path
    
    def play_text_file(self, textfilename, lang):
        text = self.read_from_file(textfilename)
        self.play_text(text, lang)
    
    def export_text_file(self, textfilename, lang):
        text = self.read_from_file(textfilename)
        return self.export_text(text, lang)
    
    def toggle_pause(self):
        self.player.toggle_pause()

    def back(self):
        self.player.back()
    
    def speedup(self):
        self.player.set_speed(self.player.speed + self.config.speed_increment)

    def speeddown(self):
        self.player.set_speed(self.player.speed - self.config.speed_increment)
