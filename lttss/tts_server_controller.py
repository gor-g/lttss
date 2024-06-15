from tts_service import TTSService
from flask import Flask, request, make_response
import os
import signal
from utils import get_os_api


PID = os.getpid()
app = Flask(__name__)

config = get_os_api().get_config()

tts_service = None


@app.route('/read_from_file', methods=['POST'])
def read_from_file():
    data = request.json
    tts_service.play_text_file(data["textfilename"])
    return make_response('', 200)

@app.route('/speedup', methods=['POST'])
def speedup():
    new_speed = tts_service.speedup()
    return make_response(
        f"{new_speed:.2f}"
        , 200)

@app.route('/speeddown', methods=['POST'])
def speeddown():
    new_speed = tts_service.speeddown()
    return make_response(
        f"{new_speed:.2f}"
        , 200)

@app.route('/export_from_file', methods=['POST'])
@app.route('/export_from_file/<lang>', methods=['POST'])
def export_from_file(lang='english'):
    data = request.json
    path = tts_service.export_text_file(data["textfilename"], lang)
    return make_response(path, 200)

@app.route('/export', methods=['POST'])
@app.route('/export/<lang>', methods=['POST'])
def export(lang='english'):
    data = request.json
    path = tts_service.export_text(data["text"], lang)
    return make_response(path, 200)

@app.route('/play_text', methods=['POST'])
@app.route('/play_text/<lang>', methods=['POST'])
def play_text(lang='english'):
    data = request.json
    tts_service.play_text(data["text"], lang)
    return make_response('', 200)

@app.route('/append_text', methods=['POST'])
@app.route('/append_text/<lang>', methods=['POST'])
def append_text(lang='english'):
    data = request.json
    tts_service.append_text(data["text"], lang)
    return make_response('', 200)

@app.route('/toggle_pause', methods=['POST'])
def toggle_pause():
    tts_service.toggle_pause()
    return make_response('', 200)

@app.route('/back', methods=['POST'])
def back():
    tts_service.back()
    return make_response('', 200)

@app.route('/uname', methods=['GET'])
def uname():
    return make_response("lttss", 200)

@app.route("/shutdown")
def shutdown():
    pid = os.getpid()
    assert pid == PID
    os.kill(pid, signal.SIGINT)
    return "shuting down lttss", 200

@app.before_request
def initialize():
    global tts_service
    if tts_service is None:
        tts_service = TTSService(config)

if __name__ == '__main__':
    app.run(port=config.port, debug=True)