from PyQt6.QtWidgets import *
from PyQt6.QtCore import QRect, QCoreApplication, Qt
from start.combox import CustomComboBox
import json
import re
from scripts.worker import Worker
from utils.netfunc import SendNetFunctions

class SendNet(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.send_net_functions = SendNetFunctions()

    def initUI(self):
        centralwidget = QWidget()
        centrallayout = QVBoxLayout(centralwidget)

        run_show_ui = QHBoxLayout()
        self.send_type = QLabel("请求类型")
        self.send_type.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.send_type.setFixedWidth(95)
        self.send_type.setFixedHeight(30)
        self.comboBox = CustomComboBox()
        self.comboBox.setFixedWidth(100)
        self.comboBox.setFixedHeight(30)
        self.comboBox.addItems(["GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS", "PATCH"])
        self.send_address = QLabel("请求地址")
        self.send_address.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.send_address.setFixedHeight(30)
        self.requests_address = QLineEdit()
        self.requests_address.setFixedHeight(28)
        self.requests_address.setPlaceholderText(" 请输入请求地址")
        self.import_data = QPushButton("导入数据")
        self.import_data.setFixedHeight(28)
        self.import_data.setFixedWidth(80)
        self.import_data.clicked.connect(self.importData)
        self.send_requests = QPushButton("发送")
        self.send_requests.clicked.connect(self.sendRequest)
        self.send_requests.setFixedWidth(80)
        self.send_requests.setFixedHeight(28)
        run_show_ui.addWidget(self.send_type)
        run_show_ui.addWidget(self.comboBox)
        run_show_ui.addWidget(self.send_address)
        run_show_ui.addWidget(self.requests_address)
        run_show_ui.addWidget(self.import_data)
        run_show_ui.addWidget(self.send_requests)
        centrallayout.addLayout(run_show_ui)

        run_show_proxy = QHBoxLayout()
        self.proxy = QLabel("代理地址")
        self.proxy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.proxy.setFixedWidth(95)
        self.proxy.setFixedHeight(30)
        self.proxy_address = QLineEdit()
        self.proxy_address.setFixedHeight(28)
        self.proxy_address.setPlaceholderText(" 请输入代理地址(xxx.xxx.xxx.xxx)...")
        self.proxy_api = QLabel("代理API")
        self.proxy_api.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.proxy_api.setFixedHeight(30)
        self.proxy_api.setFixedWidth(90)
        self.proxy_api_address = QLineEdit()
        self.proxy_api_address.setFixedHeight(28)
        self.proxy_api_address.setPlaceholderText(" 请输入代理API...")
        self.checkBox_redirect = QCheckBox("禁止重定向")
        self.checkBox_verify = QCheckBox("禁用SSL")
        run_show_proxy.addWidget(self.proxy)
        run_show_proxy.addWidget(self.proxy_address)
        run_show_proxy.addWidget(self.proxy_api)
        run_show_proxy.addWidget(self.proxy_api_address)
        run_show_proxy.addWidget(self.checkBox_redirect)
        run_show_proxy.addWidget(self.checkBox_verify)
        centrallayout.addLayout(run_show_proxy)

        run_show_post_data = QHBoxLayout()
        self.showlabel_postdata = QLabel("提交数据")
        self.showlabel_postdata.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.showlabel_postdata.setFixedWidth(95)
        self.post_data_text = QPlainTextEdit()
        self.post_data_text.setPlaceholderText("请输入请求体内容...")
        self.post_data_text.setFixedHeight(120)
        run_show_post_data.addWidget(self.showlabel_postdata)
        run_show_post_data.addWidget(self.post_data_text)
        centrallayout.addLayout(run_show_post_data)

        run_show_head_cookie = QHBoxLayout()
        self.showlabel_postdata = QLabel("协议数据")
        self.showlabel_postdata.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.showlabel_postdata.setFixedWidth(95)
        self.post_data_header = QPlainTextEdit("Accept: */*\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
        self.post_data_header.setFixedHeight(150)
        self.post_data_header.setPlaceholderText("请输入协议请求头数据...")
        self.showlabel_cookie = QLabel("Cookie\n数据")
        self.showlabel_cookie.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.showlabel_cookie.setFixedWidth(95)
        self.cookie_data_text = QPlainTextEdit()
        self.cookie_data_text.setPlaceholderText("请输入Cookie内容数据...")
        self.cookie_data_text.setFixedHeight(150)
        run_show_head_cookie.addWidget(self.showlabel_postdata)
        run_show_head_cookie.addWidget(self.post_data_header)
        run_show_head_cookie.addWidget(self.showlabel_cookie)
        run_show_head_cookie.addWidget(self.cookie_data_text)
        centrallayout.addLayout(run_show_head_cookie)

        show_result = QHBoxLayout()
        self.start_page_result = QTabWidget()

        self.response_text = QWidget()
        text_layout = QVBoxLayout(self.response_text)
        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlaceholderText("返回正文数据...")
        text_layout.addWidget(self.text_edit)
        self.start_page_result.addTab(self.response_text, "响应正文")

        self.response_header = QWidget()
        header_layout = QVBoxLayout(self.response_header)
        self.header_edit = QPlainTextEdit()
        self.header_edit.setPlaceholderText("返回协议头数据...")
        header_layout.addWidget(self.header_edit)
        self.start_page_result.addTab(self.response_header, "返回协议头")

        self.response_cookie = QWidget()
        cookie_layout = QVBoxLayout(self.response_cookie)
        self.cookie_edit = QPlainTextEdit()
        self.cookie_edit.setPlaceholderText("返回Cookie数据...")
        cookie_layout.addWidget(self.cookie_edit)
        self.start_page_result.addTab(self.response_cookie, "返回Cookie")

        show_result.addWidget(self.start_page_result)
        centrallayout.addLayout(show_result)

        end_status = QHBoxLayout()
        self.send_status = QLabel("请求状态：")
        self.send_status.setFixedHeight(30)
        self.copy_code = QPushButton("复制响应")
        self.copy_code.setFixedHeight(28)
        self.copy_code.setFixedWidth(80)
        self.generate_code = QPushButton("生成代码")
        self.generate_code.setFixedHeight(28)
        self.generate_code.setFixedWidth(80)
        self.copy_code.clicked.connect(self.copyCodeResult)
        self.generate_code.clicked.connect(self.GenerCode)
        end_status.addWidget(self.send_status)
        end_status.addWidget(self.copy_code)
        end_status.addWidget(self.generate_code)
        centrallayout.addLayout(end_status)

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

    def sendRequest(self):
        try:
            url = self.requests_address.text()
            if url:
                data = self.post_data_text.toPlainText()
                headers = self.send_net_functions.parseHeaders(self.post_data_header.toPlainText())
                cookies = self.send_net_functions.parseCookies(self.cookie_data_text.toPlainText())
                proxy = self.proxy_address.text()
                method = self.comboBox.currentText()
                proxy_api = self.proxy_api_address.text()
                check_verify = not self.checkBox_verify.isChecked()
                check_allow_redirects = not self.checkBox_redirect.isChecked()
                proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
                try:
                    self.text_edit.setPlainText("正在请求数据...")
                    self.send_status.setText("请求状态：正在请求...")
                    self.worker = Worker(url, method, data, headers, cookies, proxies, proxy_api, check_verify, check_allow_redirects)
                    self.worker.finished.connect(self.displayResponse)
                    self.worker.start()
                except Exception as e:
                    self.text_edit.setPlainText(f"Error: {str(e)}")
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Warning)
                msg_box.setWindowTitle("警告")
                msg_box.setText("请输入请求地址")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.setStyleSheet("")
                msg_box.exec()
        except:
            pass

    def displayResponse(self, response_text, headers, cookies, time, statuscode, size):
        response_data = self.send_net_functions.displayResponse(response_text, headers, cookies, time, statuscode, size)
        self.text_edit.setPlainText(response_data['formatted_text'])
        self.send_status.setText(response_data['status_text'])

        if response_data['headers']:
            self.header_edit.setPlainText(json.dumps(dict(response_data['headers']), indent=4, ensure_ascii=False))
        if response_data['cookies']:
            self.cookie_edit.setPlainText(json.dumps(dict(response_data['cookies']), indent=4, ensure_ascii=False))

    def importData(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("导入数据")
        dialog.resize(500, 400)
        layout = QVBoxLayout()
        data_input = QPlainTextEdit()
        layout.addWidget(data_input)
        button_layout = QHBoxLayout()
        import_curl_button = QPushButton("导入Curl")
        import_raw_button = QPushButton("导入Raw")
        cancel_button = QPushButton("取消")
        button_layout.addWidget(import_curl_button)
        button_layout.addWidget(import_raw_button)
        button_layout.addWidget(cancel_button)
        import_curl_button.setMinimumSize(25, 25)
        import_raw_button.setMinimumSize(25, 25)
        cancel_button.setMinimumSize(25, 25)
        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        def on_import_curl():
            curl_command = data_input.toPlainText()
            curl_data = self.send_net_functions.importCurl(curl_command)
            self.requests_address.setText(curl_data['url'])
            self.comboBox.setCurrentText(curl_data['method'])
            self.post_data_text.setPlainText(curl_data['data'] or "")
            self.post_data_header.setPlainText("\n".join([f"{k}: {v}" for k, v in curl_data['headers'].items()]))
            self.cookie_data_text.setPlainText("; ".join([f"{k}={v}" for k, v in curl_data['cookies'].items()]))
            self.proxy_address.setText(curl_data['proxy'] or "")
            dialog.accept()

        def http_protocol(url):
            if not re.match(r'^https?://', url):
                return False
            return True

        def on_import_raw():
            raw_data = data_input.toPlainText()
            raw_data_dict = self.parse_raw_data(raw_data)
            if http_protocol(raw_data_dict['url']):
                url = raw_data_dict['url']
            else:
                url = "https://" + raw_data_dict['headers']['Host'] + raw_data_dict['url']
            self.requests_address.setText(url)
            self.comboBox.setCurrentText(raw_data_dict['method'])
            self.post_data_text.setPlainText(raw_data_dict['data'] or "")
            self.post_data_header.setPlainText("\n".join([f"{k}: {v}" for k, v in raw_data_dict['headers'].items()]))
            self.cookie_data_text.setPlainText("; ".join([f"{k}={v}" for k, v in raw_data_dict['cookies'].items()]))
            self.proxy_address.setText(raw_data_dict['proxy'] or "")
            dialog.accept()

        def on_cancel():
            dialog.reject()

        import_curl_button.clicked.connect(on_import_curl)
        import_raw_button.clicked.connect(on_import_raw)
        cancel_button.clicked.connect(on_cancel)

        dialog.exec()

    def parse_raw_data(self, raw_data):
        lines = raw_data.split('\n')
        method, url, _ = lines[0].split(' ')
        headers = {}
        cookies = {}
        data = None
        for line in lines[1:]:
            if line.strip() == '':
                break
            key, value = line.split(': ', 1)
            if key == 'Cookie':
                for cookie in value.split('; '):
                    k, v = cookie.split('=', 1)
                    cookies[k] = v
            else:
                headers[key] = value
        return {
            'method': method,
            'url': url,
            'headers': headers,
            'cookies': cookies,
            'data': data,
            'proxy': None
        }

    def GenerCode(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("请求代码生成 · 双击编程语言")
        dialog.resize(500, 400)
        layout = QVBoxLayout(dialog)

        list_code = QListWidget(dialog)
        programme_list = [
            "Python - Requests",
            "PHP - cURL",
            "Java - OKHttp",
            "Shell - cURL"
        ]
        for item in programme_list:
            list_code.addItem(item)
        layout.addWidget(list_code)

        list_code.itemDoubleClicked.connect(self.on_item_double_clicked)

        dialog.exec()

    def on_item_double_clicked(self, item):
        url = self.requests_address.text()
        method = self.comboBox.currentText()
        cookies_text = self.cookie_data_text.toPlainText()
        headers = json.dumps(self.send_net_functions.parseHeaders(self.post_data_header.toPlainText()), indent=4)
        cookies = json.dumps(self.send_net_functions.parseCookies(self.cookie_data_text.toPlainText()), indent=4)
        data = self.post_data_text.toPlainText() if self.post_data_text.toPlainText() else ""
        check_verify = self.checkBox_verify.isChecked()
        check_allow_redirects = self.checkBox_redirect.isChecked()
        code = self.send_net_functions.generate_code_for_language(item.text(), url, method, headers, cookies, data, check_verify, check_allow_redirects)
        self.show_generated_code(code, item.text())

    def show_generated_code(self, code, language):
        code_dialog = QDialog(self)
        code_dialog.setWindowTitle(f"生成代码 · {language}")
        code_dialog.resize(800, 600)
        layout = QVBoxLayout(code_dialog)
        code_text = QPlainTextEdit(code_dialog)
        code_text.setPlainText(code)
        code_text.setReadOnly(True)
        layout.addWidget(code_text)
        code_dialog.exec()

    def copyCodeResult(self):
        text = self.text_edit.toPlainText()
        QApplication.clipboard().setText(text)