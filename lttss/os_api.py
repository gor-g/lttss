import os
import subprocess
from config import LTTSSConfig

class OSAPI:
    def get_config(self) -> LTTSSConfig:
        pass

    def read_clipboard_content(self)->str:
        pass

    def notify(self, message) -> None:
        print("notify OSAPI")
        pass

class LinuxAPI(OSAPI):
    def __init__(self):
        self.uname = os.uname()
    
    def get_config(self) -> LTTSSConfig:
        config = LTTSSConfig(os.path.expanduser("~")+"/.config/lttss/lttss-config.json")
        self.clipboard = config.clipboard
        return config

    def read_clipboard_content(self):
        if self.clipboard in ["copy", "clipboard"]:
            data = subprocess.check_output(['xclip', '-selection', 'clipboard', '-o']).decode()

        elif self.clipboard in ["selection", "primary"]:
            data = subprocess.check_output(['xclip', '-selection', 'primary', '-o']).decode()
        
        else:
            raise Exception("Invalid clipboard type.")
        
        return data
        
    def notify(self, message):
        res =  subprocess.run(["notify-send",  message])
        if res.returncode != 0:
            raise Exception(f"notify-send failed with error : {res.stderr}")


class WindowsAPI(OSAPI):
    def __init__(self):
        raise Exception("The WindowsAPI class implementation has not been tested on a Windows machine.")
    
    def get_config(self) -> LTTSSConfig:
        config = LTTSSConfig(os.path.expanduser("~")+"/lttss/lttss-config.json")
        self.clipboard = config.clipboard
        return config

    def read_clipboard_content(self):
        if self.clipboard in ["copy", "clipboard"]:
            data = subprocess.check_output(['clip', '/out']).decode()

        elif self.clipboard in ["selection", "primary"]:
            raise Exception("Selection buffer is not supported on Windows.")
        
        else:
            raise Exception("Invalid clipboard type.")
        
        return data
        
    def notify(self, message):
        subprocess.run(["powershell", "-Command", f"New-BurntToastNotification -Text '{message}'"])


class MacOSAPI(OSAPI):
    def __init__(self):
        raise Exception("The macOSAPI class implementation has not been tested on a macOS machine.")
    
    def get_config(self) -> LTTSSConfig:
        config = LTTSSConfig(os.path.expanduser("~")+"/lttss/lttss-config.json")
        self.clipboard = config.clipboard
        return config

    def read_clipboard_content(self):
        if self.clipboard in ["copy", "clipboard"]:
            data = subprocess.check_output(['pbpaste']).decode()

        elif self.clipboard in ["selection", "primary"]:
            raise Exception("Selection buffer is not supported on macOS.")
        
        else:
            raise Exception("Invalid clipboard type.")
        
        return data
        
    def notify(self, message):
        subprocess.run(["osascript", "-e", f'display notification "{message}" with title "LTTSS"'])