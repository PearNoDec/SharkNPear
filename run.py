import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QMessageBox, QPushButton
from PyQt6.QtGui import QIcon
from start.sidebar import Sidebar
from start.stack import CustomStackedWidget
from scripts.update import UpdateVersion
import webbrowser

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.checkForUpdates()

    def initUI(self):
        self.setWindowTitle('SharkNPear - Tools')
        self.setGeometry(100, 100, 1000, 655)

        main_layout = QHBoxLayout()
        self.sidebar = Sidebar()
        self.sidebar.currentRowChanged.connect(self.display)

        self.stack = CustomStackedWidget()

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

    def display(self, index):
        self.stack.setCurrentIndex(index)

    def checkForUpdates(self):
        self.update_thread = UpdateVersion("")
        self.update_thread.version_signal.connect(self.promptUpdate)
        self.update_thread.start()

    def promptUpdate(self, is_new_version, new_version, downloadlink, journal):
        if is_new_version:
            msg = QMessageBox()
            msg.setWindowTitle("检测到新版本")
            msg.setText(f"当前版本：{self.update_thread.now_version}\n检测版本：{new_version}\n更新日志：\n{journal}")
            yes_button = QPushButton("更新")
            no_button = QPushButton("取消")

            msg.addButton(yes_button, QMessageBox.ButtonRole.YesRole)
            msg.addButton(no_button, QMessageBox.ButtonRole.NoRole)

            yes_button.clicked.connect(lambda: self.handleUpdateResponse(True, downloadlink))
            msg.exec()

    def handleUpdateResponse(self, button, link):
        if button:
            webbrowser.open(link)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('resources/icon.ico')))
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
