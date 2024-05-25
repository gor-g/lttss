import json
from pathlib import Path
from warnings import warn

class LTTSSConfig():
    def __init__(self, path):
        config_json = self.load_from_json(path)
        self.models = config_json["models"]
        self.fallback_lang = config_json["fallback_lang"]
        self.data_dir_path = Path(config_json["data_dir_path"])
        self.models_dir_path = self.data_dir_path / "models"
        self.intersentence_silence_wav_path = self.data_dir_path / "intersentence_silence.wav"
        self.initial_silence_wav_path = self.data_dir_path / "initial_silence.wav"
        self.export_dir_path = Path(config_json["export_dir_path"])
        self.tmp_dir_path = Path(config_json["tmp_dir_path"])

        self.mpv_socket_file_name = Path(config_json["mpv_socket_file_name"])
        self.to_play_dir_name = Path(config_json["to_play_dir_name"])

        self.to_play_dir_path = self.tmp_dir_path / self.to_play_dir_name
        self.mpv_socket_dir_path = self.tmp_dir_path / self.mpv_socket_file_name

        self.port = config_json["port"]

        self.default_speed = config_json["default_speed"]
        self.speed_increment = config_json["speed_increment"]

        self.intersentence_pause_duration = config_json["intersentence_pause_duration"]
        self.initial_latency_duration = config_json["initial_latency_duration"]
        self.clipboard = config_json["clipboard"]

        if "export_format" in config_json:
            self.export_format : str = config_json["export_format"].lower()
            if self.export_format not in ["wav", "mp3"]:
                warn(f"Export format {self.export_format} is not supported. Defaulting to wav.")
                self.export_format = "wav"
        else:
            self.export_format = "wav"

        self.ffmpeg_path = config_json["ffmpeg_path"]


    def load_from_json(self, path):
        with open(str(path)) as f:
            config = json.load(f)
        return config