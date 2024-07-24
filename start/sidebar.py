from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtGui import QColor, QBrush, QIcon
from PyQt6.QtCore import Qt, QSize
import sys
import os

class Sidebar(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(140)
        self.setIconSize(QSize(20, 20))
        self.setStyleSheet("""
            QListWidget {
                background-color: #FFFFFF;
                color: black;
                border-radius: 10px;
                border: 1px solid #ccc;
                outline: none;
                padding: 1px;
            }
            QListWidget::item {
                padding: 5px;
                outline: none;
            }
            QListWidget::item:selected {
                background-color: #EEEEEE;
                color: black;
                outline: none;
            }
        """)

        self.add_item("网络请求发送", resource_path("resources/sendnet.png"))
        self.add_item("Json解析", resource_path("resources/json.png"))
        self.add_item("编码/加解密", resource_path("resources/coding.png"))
        self.add_item("WebSocket", resource_path("resources/websocket.png"))
        self.add_item("正则表达式", resource_path("resources/regular.png"))
        self.add_item("网络抓包", resource_path("resources/capture.png"))
        self.add_item("其他工具", resource_path("resources/tools.png"))
        self.add_item("关于作者", resource_path("resources/people.png"))

    def add_item(self, text, icon_path):
        item = QListWidgetItem(text)
        item.setIcon(QIcon(icon_path))
        item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.addItem(item)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)