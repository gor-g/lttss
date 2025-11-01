import os
import shutil
import platform

def initialize():
    """Ensure user config and model directories exist, only on Linux."""
    # Check if running on Linux
    if platform.system().lower() != "linux":
        print("Non-Linux system detected — skipping user setup.")
        return

    # Define paths
    home = os.path.expanduser("~")
    user_config_dir = os.path.join(home, ".config", "lttss")
    user_config_file = os.path.join(user_config_dir, "config.json")
    user_data_dir = os.path.join(home, ".lttss")

    # Source data path (from package installation or local dev)
    local_data = os.path.join(os.path.dirname(__file__), "..", "data")
    system_data = "/usr/share/lttss"
    data_dir = system_data if os.path.exists(system_data) else local_data

    # Ensure config directory exists
    os.makedirs(user_config_dir, exist_ok=True)

    # Copy default config if missing
    default_config = os.path.join(data_dir, "default-config.json")
    if not os.path.exists(user_config_file):
        if os.path.exists(default_config):
            shutil.copy(default_config, user_config_file)
            print(f"Created user config: {user_config_file}")
        else:
            print(f"Warning: default config not found at {default_config}")
    else:
        print("Config already exists, skipping copy.")

    # Copy models directory if missing
    src_models = os.path.join(data_dir, "models")
    dst_models = os.path.join(user_data_dir, "models")

    if not os.path.exists(dst_models):
        if os.path.exists(src_models):
            os.makedirs(user_data_dir, exist_ok=True)
            shutil.copytree(src_models, dst_models, dirs_exist_ok=True)
            print(f"Copied models to {dst_models}")
        else:
            print(f"Warning: models directory not found at {src_models}")
    else:
        print("Models already exist, skipping copy.")
