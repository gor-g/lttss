import os
from tts_server_config import TTSServerConfig
from piper.voice import PiperVoice
import nltk
import time
from langdetect import detect
import wave
from player_service import MPV

class TTSService():
    def __init__(self):
        self.config : TTSServerConfig = TTSServerConfig()
        self.load_models()
        os.makedirs(self.config.tmp_dir_path, exist_ok=True)
        os.makedirs(self.config.export_dir_path, exist_ok=True)
        os.makedirs(self.config.to_play_dir_path, exist_ok=True)
        self.player : MPV  = MPV(self.config.mpv_socket_dir_path, self.config.default_speed)
        self.player.run()
        if not nltk.data.find('tokenizers/punkt'):
            nltk.download('punkt')


    def load_models(self):
        self.models : dict = dict()
        for lang, modelfilename in self.config.models.items():
            self.models[lang] = PiperVoice.load(self.config.models_dir_path / modelfilename)
        self.models['fallback'] = self.models[self.config.fallback_lang]

    def detect_language(self, text):
        try:
            lang = detect(text)
            if lang in self.models.keys():
                return lang
            else:
                return 'fallback'
        except Exception as e:
            print(e)
            return 'fallback'

    def make_tmp_wav_path(self):
        return f"{self.config.to_play_dir_path}/voice-{time.time_ns()}.wav"
    
    def make_export_wav_path(self):
        return f"{self.config.export_dir_path}/voice-{time.time_ns()}.wav"
    
    def generate_audio(self, lang, text, path):
        wav_file = wave.open(path, 'w')
        try:
            self.models[lang].synthesize(text, wav_file)
        finally:
            wav_file.close()
        return path
    
    def read_from_file(self, textfilename):
        with open(textfilename, 'r') as f:
            text = f.read()
        return text
    
    def tokenize(self, text):
        sentences = nltk.tokenize.sent_tokenize(text)
        return sentences
    
    def play(self, sentence):
        lang = self.detect_language(sentence)
        path = self.make_tmp_wav_path()
        self.generate_audio(lang, sentence, path)
        self.player.play(path)

    def play_sentences(self, sentences):
        sentence = sentences.pop(0)
        path = self.make_tmp_wav_path()
        lang = self.detect_language(sentence)
        self.generate_audio(lang, sentence, path)
        self.player.load_new_sequance_tip(path)
        for sentence in sentences:
            path = self.make_tmp_wav_path()
            lang = self.detect_language(sentence)
            self.generate_audio(lang, sentence, path)
            self.player.append(path)
        return

    def append_sentences(self, sentences):
        for sentence in sentences:
            path = self.make_tmp_wav_path()
            self.generate_audio(sentence, path)
            self.player.append(path)
        return
    
    def play_text(self, text):
        sentences = self.tokenize(text)
        self.play_sentences(sentences)

    def export_text(self, text):
        lang = self.detect_language(text)
        path = self.make_export_wav_path()
        self.generate_audio(lang, text, path)
        return path
    
    def play_text_file(self, textfilename):
        text = self.read_from_file(textfilename)
        self.play_text(text)
    
    def export_text_file(self, textfilename):
        text = self.read_from_file(textfilename)
        return self.export_text(text)
    
    def speedup(self):
        self.player.set_speed(self.player.speed + self.config.speed_increment)

    def speeddown(self):
        self.player.set_speed(self.player.speed - self.config.speed_increment)
