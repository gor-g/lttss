import os
from pathlib import Path


def normalize_path(path: str | Path)->str: 
    return os.path.expanduser(str(path))
