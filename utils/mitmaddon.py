from mitmproxy import http
from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster
import chardet
import json

class MitmAddon:
    def __init__(self, gui):
        self.gui = gui
        self.flows = {}

    def request(self, flow: http.HTTPFlow) -> None:
        self.flows[flow.id] = flow

    def response(self, flow: http.HTTPFlow) -> None:
        if flow.id in self.flows:
            link = f"https://{flow.request.host}{flow.request.path}"
            status = str(flow.response.status_code) if flow.response else "N/A"
            req_type = flow.request.method
            ret_type = flow.response.headers.get("Content-Type", "N/A") if flow.response else "N/A"
            req_time = f"{flow.response.timestamp_end - flow.request.timestamp_start:.2f}秒"

            request_raw = f"{flow.request.method} {link} {flow.request.http_version}\n"
            request_raw += "\n".join(f"{k}: {v}" for k, v in flow.request.headers.items())
            if flow.request.method == "POST":
                request_raw += f"\n\n{self.decode_body(flow.request.content)}"

            request_headers = "\n".join(f"{k}: {v}" for k, v in flow.request.headers.items())
            request_body = self.decode_body(flow.request.content)

            response_raw = f"{flow.response.http_version} {flow.response.status_code} {flow.response.reason}\n"
            response_raw += "\n".join(f"{k}: {v}" for k, v in flow.response.headers.items())
            response_raw += f"\n\n{self.decode_body(flow.response.content)}"

            response_headers = "\n".join(f"{k}: {v}" for k, v in flow.response.headers.items())
            response_body = self.decode_body(flow.response.content)

            details = {
                'request_raw': request_raw,
                'request_headers': request_headers,
                'request_body': request_body,
                'response_raw': response_raw,
                'response_headers': response_headers,
                'response_body': response_body,
            }

            self.gui.add_packet_signal.emit(link, status, req_type, ret_type, str(req_time), details)
            del self.flows[flow.id]

    def decode_body(self, body):
        if body:
            detected_encoding = chardet.detect(body)
            try:
                decoded_body = body.decode(detected_encoding['encoding'])
            except (UnicodeDecodeError, TypeError):
                decoded_body = body.decode('utf-8', errors='ignore')

            try:
                json_body = json.loads(decoded_body)
                return json.dumps(json_body, indent=4, ensure_ascii=False)
            except json.JSONDecodeError:
                return decoded_body
        return ""