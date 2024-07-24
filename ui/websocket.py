from PyQt6.QtWidgets import *
from PyQt6.QtCore import QCoreApplication, Qt
from scripts.websocket import WebSocketThread

class WebSocket(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread = None
        self.is_connected = False
        self.initUI()

    def initUI(self):
        centralwidget = QWidget()
        centrallayout = QVBoxLayout(centralwidget)

        show_ui_websocket = QHBoxLayout()
        self.lable_web = QLabel("WebSocket地址")
        self.lable_web.setFixedHeight(30)
        self.show_text = QLineEdit()
        self.show_text.setFixedHeight(30)
        self.show_text.setPlaceholderText(" 请输入WebSocket地址")
        self.button_connect = QPushButton("连接")
        self.button_connect.setFixedHeight(30)
        self.button_connect.setFixedWidth(80)
        self.button_send = QPushButton("发送")
        self.button_send.setFixedHeight(30)
        self.button_send.setFixedWidth(80)
        self.button_send.clicked.connect(self.send_message)
        self.button_connect.clicked.connect(self.toggle_connection)
        show_ui_websocket.addWidget(self.lable_web)
        show_ui_websocket.addWidget(self.show_text)
        show_ui_websocket.addWidget(self.button_connect)
        show_ui_websocket.addWidget(self.button_send)
        centrallayout.addLayout(show_ui_websocket)

        run_show_message_header = QVBoxLayout()
        self.showlabel_message = QLabel("发送消息")
        self.showlabel_message.setFixedWidth(95)
        self.showlabel_message.setFixedHeight(30)
        self.post_data_message = QPlainTextEdit()
        self.post_data_message.setPlaceholderText("请输入发送消息数据...")
        self.post_data_message.setFixedHeight(120)
        self.showlabel_header = QLabel("请求协议")
        self.showlabel_header.setFixedWidth(95)
        self.showlabel_header.setFixedHeight(30)
        self.header_data_text = QPlainTextEdit("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
        self.header_data_text.setPlaceholderText("请输入请求协议内容数据...")
        self.header_data_text.setFixedHeight(120)
        run_show_message_header.addWidget(self.showlabel_message)
        run_show_message_header.addWidget(self.post_data_message)
        run_show_message_header.addWidget(self.showlabel_header)
        run_show_message_header.addWidget(self.header_data_text)
        centrallayout.addLayout(run_show_message_header)

        run_show_message_result = QVBoxLayout()
        self.reception_message = QLabel("接收数据消息区")
        self.reception_message.setFixedWidth(130)
        self.reception_message.setFixedHeight(30)
        self.message_list = QListWidget()
        run_show_message_result.addWidget(self.reception_message)
        run_show_message_result.addWidget(self.message_list)
        centrallayout.addLayout(run_show_message_result)

        self.setCentralWidget(centralwidget)

        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            QPlainTextEdit {
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px;
            }
            QLineEdit {
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            QWidget {
                margin-top: 0px;
                margin-left: 1px;
            }

            QTabWidget, QTabWidget::tab-bar, QTabWidget::pane {
                border-radius: 0px;
                margin-top: 0px;
                margin-left: 2px;
            }

            QPushButton {
                background-color: #6699FF;
                color: white;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #3366CC;
                color: white;
            }

            QListWidget {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px;
                font-size: 12px;
            }

            QListWidget::item {
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 12px;
                padding: 4px;
                margin: 1px;
                color: black;
            }

        """)

    def toggle_connection(self):
        if not self.is_connected:
            self.connect_websocket()
        else:
            self.disconnect_websocket()

    def connect_websocket(self):
        try:
            url = self.show_text.text().strip()
            if url:
                self.thread = WebSocketThread(url)
                self.thread.message_signal.connect(self.display_message)
                self.thread.start()
                self.is_connected = True
                self.button_connect.setText("断开")
                item = QListWidgetItem('WebSocket connected')
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.message_list.addItem(item)
                self.message_list.clear()
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Warning)
                msg_box.setWindowTitle("警告")
                msg_box.setText("请输入WebSocket地址")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.setStyleSheet("")
                msg_box.exec()
        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("错误")
            msg_box.setText("连接失败: " + str(e))
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.setStyleSheet("")
            msg_box.exec()

    def disconnect_websocket(self):
        if self.thread:
            self.thread.message_signal.disconnect(self.display_message)
            self.thread.close()
            self.thread = None
        self.is_connected = False
        self.button_connect.setText("连接")
        item = QListWidgetItem('WebSocket disconnected')
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.message_list.addItem(item)

    def send_message(self):
        if self.is_connected:
            message = self.post_data_message.toPlainText()
            if message.strip():
                item = QListWidgetItem("Send: " + message)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.message_list.addItem(item)
                self.thread.send_message(message)

    def display_message(self, message):
        item = QListWidgetItem(message)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.message_list.addItem(item)

    def closeEvent(self, event):
        if self.thread:
            self.thread.close()
        super().closeEvent(event)