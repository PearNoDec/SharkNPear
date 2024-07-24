from PyQt6.QtWidgets import QStackedWidget, QStackedLayout
from ui.sendnet import SendNet
from ui.jsonparse import JsonParse
from ui.encipherment import Encipherment
from ui.websocket import WebSocket
from ui.regularexpression import RegularExpression
from ui.homeinfo import HomeInfo
from ui.othertools import OtherTools
from ui.packetsniffer import PacketSniffer
import os
import sys

class CustomStackedWidget(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.addWidget(SendNet())
        self.addWidget(JsonParse())
        self.addWidget(Encipherment())
        self.addWidget(WebSocket())
        self.addWidget(RegularExpression())
        self.addWidget(PacketSniffer())
        self.addWidget(OtherTools())
        self.addWidget(HomeInfo())

        icondown = resource_path("resources\\down.png").replace("\\", "/")
        iconup = resource_path("resources\\up.png").replace("\\", "/")

        self.setStyleSheet(f"""
            QStackedWidget {{
                border-radius: 10px;
                background-color: white;
                border: 1px solid #ccc;
            }}
            QLabel {{
                padding: 20px;
                font-size: 16px;
            }}

            QComboBox {{
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 5px 10px;
                background-color: white;
                selection-background-color: #FFFFFF;
                selection-color: white;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                border-left-width: 1px;
                border-left-color: #FFFFFF;
                border-left-style: solid;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }}
            QComboBox::down-arrow {{
                image: url({icondown});
                width: 16px;
                height: 14px;
                margin-right: 5px;
            }}
            QComboBox[popupShown="true"]::down-arrow {{
                image: url({iconup});
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid #CCCCCC;
                background-color: #EEEEEE;
                selection-background-color: #FFFFFF;
                selection-color: white;
                outline: none;
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: #BBBBBB;
                outline: none;
            }}
            QComboBox QAbstractItemView::item:selected {{
                outline: none;
            }}
        """)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)