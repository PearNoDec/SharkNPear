from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QDesktopServices, QCursor, QFont
import os
import sys

class ClickableLabel(QLabel):
    def __init__(self, text, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.setText(text)
        self.setFixedHeight(60)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("font-size: 12pt;")

    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("font-size: 12pt; background-color: #EEEEEE;")
        super(ClickableLabel, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.setStyleSheet("font-size: 12pt; background-color: none;")
        super(ClickableLabel, self).leaveEvent(event)

    def mousePressEvent(self, event):
        self.linkActivated.emit(self.text())
        super(ClickableLabel, self).mousePressEvent(event)

class HomeInfo(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread = None
        self.is_connected = False
        self.initUI()

    def initUI(self):
        centralwidget = QWidget()
        centrallayout = QVBoxLayout(centralwidget)

        show_ui_title = QHBoxLayout()
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(150, 150)
        self.image_label.setScaledContents(True)
        pixmap = QPixmap(resource_path('resources\\icon.png').replace("\\", "/"))
        self.image_label.setPixmap(pixmap)
        show_ui_title.addWidget(self.image_label)

        show_text_uivb = QVBoxLayout()
        self.lable_web = QLabel("开发者：PearNo")
        self.lable_web.setFixedHeight(30)
        show_text_uivb.addWidget(self.lable_web)

        self.lable_web_time = QLabel("程序日期：2024年07月13日开发")
        self.lable_web_time.setFixedHeight(30)
        show_text_uivb.addWidget(self.lable_web_time)

        self.lable_web_info = QLabel("项目介绍：ShareNPear是一个基于Python+PyQt6的GUI桌面应用，程序功能还在持续添加...")
        self.lable_web_info.setFixedHeight(30)
        show_text_uivb.addWidget(self.lable_web_info)

        show_ui_title.addLayout(show_text_uivb)
        centrallayout.addLayout(show_ui_title)

        show_add_flex = QHBoxLayout()

        self.label_tencent = ClickableLabel("加入交流群")
        self.label_tencent.linkActivated.connect(self.open_link)
        self.label_website = ClickableLabel("API官方网址")
        self.label_website.linkActivated.connect(self.open_link)
        self.label_github = ClickableLabel("GitHub地址")
        self.label_github.linkActivated.connect(self.open_link)
        show_add_flex.addWidget(self.label_tencent)
        show_add_flex.addWidget(self.label_website)
        show_add_flex.addWidget(self.label_github)
        centrallayout.addLayout(show_add_flex)


        show_main_info = QHBoxLayout()
        self.lable_main = QLabel("暂无介绍呀~")
        self.lable_main.setAlignment(Qt.AlignmentFlag.AlignTop)
        show_main_info.addWidget(self.lable_main)
        centrallayout.addLayout(show_main_info)

        self.setCentralWidget(centralwidget)

        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            QTextEdit {
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px;
            }
            QLineEdit {
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 2px;
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

    def open_link(self, url):
        if url == "加入交流群":
            QDesktopServices.openUrl(QUrl("https://qm.qq.com/q/Ww7VVYMgWi"))
        elif url == "API官方网址":
            QDesktopServices.openUrl(QUrl("https://api.pearktrue.cn/"))
        elif url == "GitHub地址":
            QDesktopServices.openUrl(QUrl("https://github.com/PearNoDec/SharkNPear/"))
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)