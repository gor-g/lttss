
import sounddevice as sd
import soundfile as sf
import wave
import os
from piper.voice import PiperVoice
from flask import Flask, request, make_response

from lttss.player_service import MPV

import nltk

import time

from langdetect import detect

if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt')


def detect_language(text):
    try:
        return detect(text)
    except:
        return "Error"


dir = "/tmp/piper_server"
os.makedirs(dir, exist_ok=True)

def make_wav_path():
    return f"{dir}/to_play-{time.time_ns()}.wav"

voicedir = os.path.expanduser('/home/storage/work/mintPiper/tools/piper/piper/') #Where onnx model files are stored on my machine
model = voicedir+"en_US-amy-low.onnx"
voice_en = PiperVoice.load(model)
model = voicedir+"fr_FR-upmc-medium.onnx"
voice_fr = PiperVoice.load(model)


player = MPV('/tmp/mpvsocket')
player.run()


def generate_audio(text, path, voice=voice_en):
    wav_file = wave.open(path, 'w')
    try:        
        voice.synthesize(text,wav_file)
    finally:
        wav_file.close()
    return path

def read_from_file(textfilenmae):
    print(textfilenmae)
    with open(textfilenmae, 'r') as f:
        text = f.read()
    return text


def tokenize(text):
    sentences = nltk.tokenize.sent_tokenize(text)
    print(sentences)
    return sentences

def play(sentences):
    sentence = sentences.pop(0)
    path = make_wav_path()
    if detect_language(sentence) == "fr":
        voice = voice_fr
    else:
        voice = voice_en
    generate_audio(sentence, path, voice)
    player.load_new_sequance_tip(path)
    for sentence in sentences:
        path = make_wav_path()
        if detect_language(sentence) == "fr":
            voice = voice_fr
        else:
            voice = voice_en
        generate_audio(sentence, path, voice)
        player.append(path)
    return


app = Flask(__name__)


@app.route('/fromfile', methods=['POST'])
def fromfile():
    data = request.json
    text = read_from_file(data["textfilename"])
    sentences =tokenize(text)
    play(sentences)
    return make_response('', 200)


@app.route('/speedup', methods=['POST'])
def speedup():
    player.set_speed(player.speed + 0.2)
    return make_response('', 200)


if __name__ == '__main__':
    app.run(port=42069, debug=True)