from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QCoreApplication, QThread, pyqtSignal
from PyQt6.QtGui import QClipboard
from scripts.sniffthread import SniffThread
from utils.mitmaddon import MitmAddon

class PacketSniffer(QMainWindow):
    add_packet_signal = pyqtSignal(str, str, str, str, str, dict)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.sniff_thread = None
        self.sniffing = False
        self.packet_id = 0
        self.port = 8888
        self.packet_details = {}

        self.add_packet_signal.connect(self.add_packet)
        self.port_input.textChanged.connect(self.port_packets)
        self.filter_input.textChanged.connect(self.filter_packets)

    def initUI(self):
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        self.port_input = QLineEdit(self)
        self.port_input.setFixedHeight(28)
        self.port_input.setPlaceholderText("端口号...")
        self.port_input.setText("8888")
        self.port_input.setFixedWidth(60)
        self.port_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.filter_input = QLineEdit(self)
        self.filter_input.setFixedHeight(28)
        self.filter_input.setPlaceholderText("请输入待过滤的数据...")
        self.toggle_sniff_button = QPushButton("开始抓包", self)
        self.clear_button = QPushButton("清空历史", self)

        self.toggle_sniff_button.setFixedWidth(80)
        self.toggle_sniff_button.setFixedHeight(28)
        self.clear_button.setFixedWidth(80)
        self.clear_button.setFixedHeight(28)

        self.toggle_sniff_button.clicked.connect(self.toggle_sniffing)
        self.clear_button.clicked.connect(self.clear_history)

        top_layout.addWidget(self.port_input)
        top_layout.addWidget(self.filter_input)
        top_layout.addWidget(self.toggle_sniff_button)
        top_layout.addWidget(self.clear_button)

        left_layout.addLayout(top_layout)

        self.packet_table = QTableWidget(self)
        self.packet_table.setColumnCount(5)
        self.packet_table.setHorizontalHeaderLabels(["链接", "状态", "请求类型", "返回类型", "请求时间"])
        self.packet_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.packet_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.packet_table.cellDoubleClicked.connect(self.show_packet_details)
        self.packet_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.packet_table.customContextMenuRequested.connect(self.show_context_menu)

        header = self.packet_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)

        header.resizeSection(1, 60)
        header.resizeSection(2, 80)
        header.resizeSection(3, 80)
        header.resizeSection(4, 80)

        left_layout.addWidget(self.packet_table)

        right_layout = QVBoxLayout()

        self.request_tabs = QTabWidget(self)
        self.request_raw_tab = QPlainTextEdit()
        self.request_headers_tab = QPlainTextEdit()
        self.request_body_tab = QPlainTextEdit()

        self.request_tabs.addTab(self.request_raw_tab, "请求Raw数据")
        self.request_tabs.addTab(self.request_headers_tab, "请求协议头")
        self.request_tabs.addTab(self.request_body_tab, "请求体")

        right_layout.addWidget(self.request_tabs)

        self.response_tabs = QTabWidget(self)
        self.response_raw_tab = QPlainTextEdit()
        self.response_headers_tab = QPlainTextEdit()
        self.response_body_tab = QPlainTextEdit()

        self.response_tabs.addTab(self.response_raw_tab, "响应Raw数据")
        self.response_tabs.addTab(self.response_headers_tab, "响应协议头")
        self.response_tabs.addTab(self.response_body_tab, "响应体")

        right_layout.addWidget(self.response_tabs)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        container = QWidget()
        container.setLayout(main_layout)

        self.setStyleSheet("""
        QPlainTextEdit {
            font-size: 12px;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 6px;
        }

        QTableWidget {
            font-size: 12px;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 6px;
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

        QLineEdit {
            font-size: 12px;
            border: 1px solid #ccc;
            border-radius: 8px;
        }
        """)
        self.setCentralWidget(container)

    def toggle_sniffing(self):
        if self.sniffing:
            self.stop_sniffing()
            self.toggle_sniff_button.setText("开始抓包")
        else:
            self.start_sniffing()
            self.toggle_sniff_button.setText("停止抓包")

    def start_sniffing(self):
        if not self.sniffing:
            self.sniffing = True
            self.sniff_thread = SniffThread(self)
            self.sniff_thread.start()

    def stop_sniffing(self):
        if self.sniffing and self.sniff_thread:
            self.sniffing = False
            self.sniff_thread.stop()
            self.sniff_thread.wait()
            self.sniff_thread = None

    def clear_history(self):
        self.packet_table.setRowCount(0)
        self.packet_id = 0
        self.packet_details.clear()

    def add_packet(self, link, status, req_type, ret_type, req_time, details):
        row_position = self.packet_table.rowCount()
        self.packet_table.insertRow(row_position)

        self.packet_table.setItem(row_position, 0, QTableWidgetItem(link))
        self.packet_table.setItem(row_position, 1, QTableWidgetItem(status))
        self.packet_table.setItem(row_position, 2, QTableWidgetItem(req_type))
        self.packet_table.setItem(row_position, 3, QTableWidgetItem(ret_type))
        self.packet_table.setItem(row_position, 4, QTableWidgetItem(req_time))

        for i in range(1, 5):
            self.packet_table.item(row_position, i).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.packet_table.setRowHeight(row_position, 20)

        self.packet_id += 1
        self.packet_details[self.packet_id] = details

    def show_packet_details(self, row, column):
        packet_id = row + 1
        details = self.packet_details.get(packet_id, None)
        if details:
            self.request_raw_tab.setPlainText(details['request_raw'])
            self.request_headers_tab.setPlainText(details['request_headers'])
            self.request_body_tab.setPlainText(details['request_body'])

            self.response_raw_tab.setPlainText(details['response_raw'])
            self.response_headers_tab.setPlainText(details['response_headers'])
            self.response_body_tab.setPlainText(details['response_body'])

    def show_context_menu(self, position):
        menu = QMenu()
        copy_curl_action = menu.addAction("复制Curl（Bash）请求")
        action = menu.exec(self.packet_table.viewport().mapToGlobal(position))
        if action == copy_curl_action:
            self.copy_curl_request()

    def copy_curl_request(self):
        selected_row = self.packet_table.currentRow()
        if selected_row >= 0:
            packet_id = selected_row + 1
            details = self.packet_details.get(packet_id, None)
            if details:
                curl_command = self.generate_curl_command(details)
                clipboard = QApplication.clipboard()
                clipboard.setText(curl_command)

    def generate_curl_command(self, details):
        request_raw = details['request_raw']
        lines = request_raw.split('\n')
        method, path, http_version = lines[0].split()
        headers = {}
        body = ""
        for line in lines[1:]:
            if line.strip() == "":
                break
            key, value = line.split(': ', 1)
            headers[key] = value
        if method == "POST":
            body = details['request_body']
        full_url = details['request_raw'].split('\n')[0].split()[1]
        curl_command = f"curl -X {method} '{full_url}'"
        for key, value in headers.items():
            curl_command += f" -H '{key}: {value}'"
        if body:
            curl_command += f" -d '{body}'"
        return curl_command

    def filter_packets(self):
        filter_text = self.filter_input.text().lower()
        for row in range(self.packet_table.rowCount()):
            packet_id = row + 1
            details = self.packet_details.get(packet_id, None)
            if details:
                request_raw = details['request_raw'].lower()
                response_raw = details['response_raw'].lower()
                if filter_text in request_raw or filter_text in response_raw:
                    self.packet_table.setRowHidden(row, False)
                else:
                    self.packet_table.setRowHidden(row, True)
            else:
                self.packet_table.setRowHidden(row, True)

    def port_packets(self):
        self.port = int(self.port_input.text())