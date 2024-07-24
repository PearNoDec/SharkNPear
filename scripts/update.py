from PyQt6.QtCore import QThread, pyqtSignal
import requests

class UpdateVersion(QThread):
    version_signal = pyqtSignal(bool, str, str, str)

    def __init__(self, ip):
        super().__init__()
        self.now_version = "v1.01"

    def run(self):
        try:
            url = "https://www.pearktrue.cn/sharknpear/"
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}, verify=False)
            response_json = response.json()
            get_version = response_json.get("version")
            if get_version == self.now_version:
                self.version_signal.emit(False, "", "", "")
            else:
                journal = response_json.get("journal")
                downloadlink = response_json.get("downloadlink")
                self.version_signal.emit(True, get_version, downloadlink, journal)
        except Exception as e:
            self.version_signal.emit(False, "", "", "")