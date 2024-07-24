from PyQt6.QtWidgets import *
from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor
import re
from utils.regularfunc import RegularExpressionFunctions

class RegularExpression(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.regex_functions = RegularExpressionFunctions(self)
        self.initUI()

    def initUI(self):
        centralwidget = QWidget()
        centrallayout = QVBoxLayout(centralwidget)

        show_ui_websocket = QHBoxLayout()
        self.lable_web = QLabel("正则表达式")
        self.lable_web.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lable_web.setFixedHeight(30)
        self.show_text = QLineEdit()
        self.show_text.setFixedHeight(30)
        self.show_text.setPlaceholderText(" 请输入待匹配的正则表达式...")
        self.show_text.textChanged.connect(self.regex_functions.regular_content)
        self.show_match = QPushButton("常用表达式")
        self.show_match.setFixedHeight(30)
        self.show_match.setFixedWidth(80)
        self.show_match.clicked.connect(self.regex_functions.show_match_ui)
        show_ui_websocket.addWidget(self.lable_web)
        show_ui_websocket.addWidget(self.show_text)
        show_ui_websocket.addWidget(self.show_match)
        centrallayout.addLayout(show_ui_websocket)

        run_show_message_header = QVBoxLayout()
        self.text_content = QPlainTextEdit()
        self.text_content.setPlaceholderText("请输入待匹配的文本数据...")
        run_show_message_header.addWidget(self.text_content)
        centrallayout.addLayout(run_show_message_header)

        show_ui_result = QHBoxLayout()
        self.marth_show = QLabel("匹配状态：待匹配...")
        self.marth_show.setFixedHeight(30)
        show_ui_result.addWidget(self.marth_show)
        centrallayout.addLayout(show_ui_result)

        self.setCentralWidget(centralwidget)

        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
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

            QPlainTextEdit {
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px;
            }

        """)