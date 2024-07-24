import websocket
from PyQt6.QtCore import QThread, pyqtSignal

class WebSocketThread(QThread):
    message_signal = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.ws = None

    def run(self):
        try:
            self.ws = websocket.WebSocketApp(self.url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
                on_open=self.on_open)
            self.ws.run_forever()
        except Exception as e:
            self.message_signal.emit(f'Error: {e}')

    def on_message(self, ws, message):
        self.message_signal.emit(message)

    def on_error(self, ws, error):
        self.message_signal.emit(f'Error: {error}')

    def on_close(self, ws, close_status_code, close_reason):
        self.message_signal.emit('WebSocket closed')

    def on_open(self, ws):
        self.message_signal.emit('WebSocket connected')

    def send_message(self, message):
        if self.ws:
            self.ws.send(message)

    def close(self):
        if self.ws:
            self.ws.close()
        self.message_signal.emit('WebSocket disconnected')
