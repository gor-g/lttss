from tts_service import TTSService
from flask import Flask, request, make_response


app = Flask(__name__)
tts_service = TTSService()


@app.route('/fromfile', methods=['POST'])
def fromfile():
    data = request.json
    tts_service.play_text_file(data["textfilename"])
    return make_response('', 200)

@app.route('/speedup', methods=['POST'])
def speedup():
    tts_service.speedup()
    return make_response('', 200)

@app.route('/speeddown', methods=['POST'])
def speeddown():
    tts_service.speeddown()
    return make_response('', 200)

@app.route('/export_from_file', methods=['POST'])
def export_from_file():
    data = request.json
    path = tts_service.export_text_file(data["textfilename"])
    return make_response(path, 200)

@app.route('/play_text', methods=['POST'])
def play_text():
    data = request.json
    tts_service.play_text(data["text"])
    return make_response('', 200)


@app.route('/uname', methods=['GET'])
def uname():
    return make_response("lttss", 200)