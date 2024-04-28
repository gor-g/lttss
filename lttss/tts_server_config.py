import json
from pathlib import Path

class TTSServerConfig():
    def __init__(self):
        config_json = self.load_from_json()
        self.models = config_json["models"]
        self.fallback_lang = config_json["fallback_lang"]
        self.data_dir_path = Path(config_json["data_dir_path"])
        self.models_dir_path = self.data_dir_path / "models"
        self.silence_wav_path = self.data_dir_path / "silence.wav"
        self.export_dir_path = Path(config_json["export_dir_path"])
        self.tmp_dir_path = Path(config_json["tmp_dir_path"])

        self.mpv_socket_dir_name = Path(config_json["mpv_socket_dir_name"])
        self.to_play_dir_name = Path(config_json["to_play_dir_name"])

        self.to_play_dir_path = self.tmp_dir_path / self.mpv_socket_dir_name
        self.mpv_socket_dir_path = self.tmp_dir_path / self.to_play_dir_name

        self.port = config_json["port"]

        self.default_speed = config_json["default_speed"]
        self.speed_increment = config_json["speed_increment"]

    def load_from_json(self):
        with open('tss-server-config.json') as f:
            config = json.load(f)
        return config