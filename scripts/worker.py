from PyQt6.QtCore import QThread, pyqtSignal
import requests
import chardet
import time
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Worker(QThread):
    finished = pyqtSignal(str, dict, dict, float, int, float)

    def __init__(self, url, method, data, headers, cookies, proxies, proxy_api, check_verify, check_allow_redirects):
        super(Worker, self).__init__()
        self.url = url
        self.method = method
        self.data = data
        self.headers = headers
        self.cookies = cookies
        self.proxies = proxies
        self.proxy_api = proxy_api
        self.check_verify = check_verify
        self.allow_redirects = check_allow_redirects

    def run(self):
        try:
            if self.proxy_api:
                get_response = requests.get(self.proxy_api, headers=self.headers).text
                ip_port_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})')
                match = ip_port_pattern.search(get_response)
                if match:
                    ip_address = match.group(1)
                    port = match.group(2)
                    self.proxies = {"http": f"http://{ip_address}:{port}", "https": f"http://{ip_address}:{port}"}
                else:
                    self.proxies = None

            start_time = time.time()
            response = requests.request(self.method, self.url, data=self.data, headers=self.headers, cookies=self.cookies, proxies=self.proxies, verify=self.check_verify, allow_redirects=self.allow_redirects)
            elapsed_time = time.time() - start_time
            detected_encoding = chardet.detect(response.content)['encoding']
            if detected_encoding:
                response_text = response.content.decode(detected_encoding)
            else:
                response_text = response.text

            response_size = len(response.content)
            size_kb = response_size / 1024
            headers = dict(response.headers)
            cookies = dict(response.cookies)
            status_code = response.status_code
            self.finished.emit(response_text, headers, cookies, elapsed_time, status_code, size_kb)
        except Exception as e:
            self.finished.emit(f"Error: {str(e)}", {}, {}, 0, 0, 0)
