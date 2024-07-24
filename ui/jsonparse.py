from PyQt6.QtWidgets import *
from PyQt6.QtCore import QRect, QCoreApplication, Qt
import json
from utils.jsonparsefunc import *

class JsonParse(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        centralwidget = QWidget()
        centrallayout = QVBoxLayout(centralwidget)

        run_buttons = QHBoxLayout()
        self.paste_json_ui = QPushButton("粘贴Json")
        self.format_json_ui = QPushButton("格式化")
        self.transferred_json_ui = QPushButton("去转义")
        self.parse_tree_ui = QPushButton("解析到树")
        self.copy_json_ui = QPushButton("复制Json")
        self.clear_json_ui = QPushButton("清空Json")
        self.paste_json_ui.setFixedHeight(28)
        self.format_json_ui.setFixedHeight(28)
        self.transferred_json_ui.setFixedHeight(28)
        self.parse_tree_ui.setFixedHeight(28)
        self.copy_json_ui.setFixedHeight(28)
        self.clear_json_ui.setFixedHeight(28)
        self.paste_json_ui.clicked.connect(self.paste_json)
        self.format_json_ui.clicked.connect(self.format_json)
        self.transferred_json_ui.clicked.connect(self.unescape_json)
        self.parse_tree_ui.clicked.connect(self.parse_to_tree)
        self.copy_json_ui.clicked.connect(self.copy_json)
        self.clear_json_ui.clicked.connect(self.clear_json)
        run_buttons.addWidget(self.paste_json_ui)
        run_buttons.addWidget(self.format_json_ui)
        run_buttons.addWidget(self.transferred_json_ui)
        run_buttons.addWidget(self.parse_tree_ui)
        run_buttons.addWidget(self.copy_json_ui)
        run_buttons.addWidget(self.clear_json_ui)
        centrallayout.addLayout(run_buttons)

        run_text_show = QHBoxLayout()
        self.input_text = QPlainTextEdit()
        self.input_text.setPlaceholderText("请在此输入Json数据...")
        self.show_tree = QTreeWidget()
        self.show_tree.setHeaderLabel("JSON解析树")
        self.show_tree.headerItem().setTextAlignment(0, Qt.AlignmentFlag.AlignCenter)
        self.show_tree.itemClicked.connect(self.on_tree_item_clicked)
        run_text_show.addWidget(self.input_text)
        run_text_show.addWidget(self.show_tree)
        centrallayout.addLayout(run_text_show)

        parse_tree_result = QHBoxLayout()
        self.result_label = QLabel("解析结果:")
        self.result_text = QLineEdit()
        self.result_text.setFixedHeight(30)

        parse_tree_result = QHBoxLayout()
        parse_tree_result.addWidget(self.result_label)
        parse_tree_result.addWidget(self.result_text)
        centrallayout.addLayout(parse_tree_result)
        self.setCentralWidget(centralwidget)

        self.setStyleSheet("""
            QPushButton {
                background-color: #6699FF;
                color: white;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #3366CC;
                color: white;
            }

            QTextEdit, QTreeWidget {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }

            QLabel {
                font-size: 12px;
            }

            QLineEdit {
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }

            QHeaderView::section {
                background-color: #6699FF;
                color: white;
                text-align: center;
            }

            QPlainTextEdit {
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px;
            }
        """)

    def format_json(self):
        format_json(self.input_text)

    def unescape_json(self):
        unescape_json(self.input_text)

    def parse_to_tree(self):
        parse_to_tree(self.input_text, self.show_tree)

    def on_tree_item_clicked(self, item):
        index_path = item.data(0, Qt.ItemDataRole.UserRole)
        self.result_text.setText(index_path)

    def copy_json(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.input_text.toPlainText())

    def clear_json(self):
        self.input_text.clear()

    def paste_json(self):
        clipboard = QApplication.clipboard()
        self.input_text.setPlainText(clipboard.text())
