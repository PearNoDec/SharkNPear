from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIntValidator
from datetime import datetime
from utils.otherfunc import *

class OtherTools(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        start_timer(self)
        generate_uuids(self)
        generate_random_strings(self)

    def initUI(self):
        centralwidget = QWidget()
        centrallayout = QVBoxLayout(centralwidget)

        show_ui_title = QHBoxLayout()
        self.time_now = QLabel("标准时间")
        self.time_now.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_now.setFixedHeight(30)
        self.time_now_text = QLineEdit()
        self.time_now_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_now_text.setFixedHeight(30)
        self.time_now_timestamp = QLabel("时间戳·秒")
        self.time_now_timestamp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_now_timestamp.setFixedHeight(30)
        self.time_now_timestamp_text = QLineEdit()
        self.time_now_timestamp_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_now_timestamp_text.setFixedHeight(30)
        self.time_now_timestamp_ms = QLabel("时间戳·毫秒")
        self.time_now_timestamp_ms.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_now_timestamp_ms.setFixedHeight(30)
        self.time_now_timestamp_ms_text = QLineEdit()
        self.time_now_timestamp_ms_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_now_timestamp_ms_text.setFixedHeight(30)
        show_ui_title.addWidget(self.time_now)
        show_ui_title.addWidget(self.time_now_text)
        show_ui_title.addWidget(self.time_now_timestamp)
        show_ui_title.addWidget(self.time_now_timestamp_text)
        show_ui_title.addWidget(self.time_now_timestamp_ms)
        show_ui_title.addWidget(self.time_now_timestamp_ms_text)
        centrallayout.addLayout(show_ui_title)

        pinyin_layout = QHBoxLayout()
        self.pinyin_label = QLabel("文字转拼音")
        self.pinyin_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pinyin_label.setFixedHeight(30)
        self.pinyin_input = QLineEdit()
        self.pinyin_input.setPlaceholderText("请输入待转换拼音的文字...")
        self.pinyin_input.textChanged.connect(lambda: convert_to_pinyin(self))
        self.pinyin_input.setFixedHeight(30)
        self.pinyin_result_label = QLabel("结果 ->")
        self.pinyin_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pinyin_result_label.setFixedHeight(30)
        self.pinyin_result_text = QLineEdit()
        self.pinyin_result_text.setPlaceholderText("转换结果...")
        self.pinyin_result_text.setFixedHeight(30)
        pinyin_layout.addWidget(self.pinyin_label)
        pinyin_layout.addWidget(self.pinyin_input)
        pinyin_layout.addWidget(self.pinyin_result_label)
        pinyin_layout.addWidget(self.pinyin_result_text)

        random_generate = QHBoxLayout()
        random_title = QVBoxLayout()
        self.random_qlabel = QLabel("随机生成字符")
        self.random_qlabel.setFixedHeight(30)
        self.random_qlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        random_setting_ui = QHBoxLayout()
        self.random_sum = QLineEdit("4")
        self.random_sum.setPlaceholderText("生成数量...")
        self.random_sum.setValidator(QIntValidator(1, 100))
        self.random_sum.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.random_sum.setFixedHeight(50)
        self.random_sum.setFixedWidth(60)
        self.random_sum_length = QLineEdit("32")
        self.random_sum_length.setPlaceholderText("生成长度...")
        self.random_sum_length.setValidator(QIntValidator(1, 100))
        self.random_sum_length.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.random_sum_length.setFixedHeight(50)
        self.random_sum_length.setFixedWidth(60)
        random_title.addWidget(self.random_qlabel)
        random_setting_ui.addWidget(self.random_sum)
        random_setting_ui.addWidget(self.random_sum_length)
        random_title.addLayout(random_setting_ui)
        random_generate.addLayout(random_title)

        random_result = QHBoxLayout()
        self.random_result_setting = QPlainTextEdit("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.random_result_setting.setPlaceholderText("设置随机字符...")
        self.random_result_setting.setFixedHeight(90)
        self.random_result_setting.textChanged.connect(lambda: generate_random_strings(self))
        self.random_result_text = QPlainTextEdit()
        self.random_result_text.setPlaceholderText("生成结果...")
        self.random_result_text.setFixedHeight(90)
        random_result.addWidget(self.random_result_setting)
        random_result.addWidget(self.random_result_text)
        random_generate.addLayout(random_result)
        centrallayout.addLayout(random_generate)

        uuid_generate = QHBoxLayout()
        uuid_title = QVBoxLayout()
        self.uuid_qlabel = QLabel("UUID生成")
        self.uuid_qlabel.setFixedHeight(30)
        self.uuid_qlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.uuid_sum = QLineEdit("4")
        self.uuid_sum.setPlaceholderText("生成数量...")
        self.uuid_sum.textChanged.connect(lambda: generate_uuids(self))
        self.uuid_sum.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.uuid_sum.setFixedHeight(50)
        self.uuid_sum.setFixedWidth(110)
        self.uuid_sum.setValidator(QIntValidator(1, 100))
        uuid_title.addWidget(self.uuid_qlabel)
        uuid_title.addWidget(self.uuid_sum)
        uuid_generate.addLayout(uuid_title)

        uuid_result = QHBoxLayout()
        self.uuid_result_text = QPlainTextEdit()
        self.uuid_result_text.setPlaceholderText("生成结果...")
        self.uuid_result_text.setFixedHeight(90)
        uuid_result.addWidget(self.uuid_result_text)
        uuid_generate.addLayout(uuid_result)
        centrallayout.addLayout(uuid_generate)

        text_comparison = QHBoxLayout()
        self.text_comparison_text = QPlainTextEdit()
        self.text_comparison_text.setPlaceholderText(" 请输入原始文本...")
        self.text_comparison_result = QPlainTextEdit()
        self.text_comparison_result.setPlaceholderText(" 请输入比对文本...")
        self.text_comparison_text.textChanged.connect(lambda: compare_texts(self))
        self.text_comparison_result.textChanged.connect(lambda: compare_texts(self))
        text_comparison.addWidget(self.text_comparison_text)
        text_comparison.addWidget(self.text_comparison_result)
        centrallayout.addLayout(text_comparison)

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

            QPushButton {
                background-color: #6699FF;
                color: white;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #3366CC;
                color: white;
            }
        """)

    def update_time(self):
        now = datetime.now()
        self.time_now_text.setText(now.strftime('%Y-%m-%d %H:%M:%S'))
        self.time_now_timestamp_text.setText(str(int(now.timestamp())))
        self.time_now_timestamp_ms_text.setText(str(int(now.timestamp() * 1000)))
