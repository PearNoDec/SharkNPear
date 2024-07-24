from PyQt6.QtWidgets import *
from PyQt6.QtCore import QCoreApplication, Qt
from start.combox import CustomComboBox
import utils.encipherfunc as ef

class Encipherment(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        self.tabWidget = QTabWidget()
        main_layout.addWidget(self.tabWidget)

        # Hash Tab
        hash_widget = QWidget()
        hash_layout = QGridLayout(hash_widget)
        self.tabWidget.addTab(hash_widget, "Hash")

        self.textEdit = QPlainTextEdit()
        self.textEdit.setPlaceholderText("请输入待Hash编码文本")
        self.textEdit.textChanged.connect(self.update_hashes)
        hash_layout.addWidget(self.textEdit, 0, 0, 1, 2)

        self.checkBox = QCheckBox("大写")
        self.checkBox.stateChanged.connect(self.update_hashes)
        hash_layout.addWidget(self.checkBox, 1, 0)

        hash_results_layout = QVBoxLayout()
        self.hash_results = {}
        for hash_type in ["MD5", "MD5_Middle", "Sha1", "Sha256", "Sha512"]:
            self.hash_results[hash_type] = QPlainTextEdit()
            self.hash_results[hash_type].setPlaceholderText(f"{hash_type}值")
            hash_results_layout.addWidget(self.hash_results[hash_type])

        hash_layout.addLayout(hash_results_layout, 0, 2, 2, 1)

        # URL Tab
        url_widget = QWidget()
        url_layout = QVBoxLayout(url_widget)
        self.tabWidget.addTab(url_widget, "Url编码")

        self.url_input = QPlainTextEdit()
        self.url_input.setPlaceholderText("请输入待编/解码的文本数据")
        url_layout.addWidget(self.url_input)

        url_buttons = QHBoxLayout()
        self.url_encode_btn = QPushButton("编码")
        self.url_decode_btn = QPushButton("解码")
        self.url_encode_btn.clicked.connect(self.url_encode)
        self.url_decode_btn.clicked.connect(self.url_decode)
        url_buttons.addWidget(self.url_encode_btn)
        url_buttons.addWidget(self.url_decode_btn)
        url_layout.addLayout(url_buttons)

        self.url_output = QPlainTextEdit()
        self.url_output.setPlaceholderText("待显示编/解码数据...")
        url_layout.addWidget(self.url_output)

        # Base64 Tab
        base64_widget = QWidget()
        base64_layout = QVBoxLayout(base64_widget)
        self.tabWidget.addTab(base64_widget, "Base64")

        self.base64_input = QPlainTextEdit()
        self.base64_input.setPlaceholderText("请输入待编/解码的文本数据")
        base64_layout.addWidget(self.base64_input)

        base64_buttons = QHBoxLayout()
        self.base64_encode_btn = QPushButton("编码")
        self.base64_decode_btn = QPushButton("解码")
        self.base64_encode_btn.clicked.connect(self.base64_encode)
        self.base64_decode_btn.clicked.connect(self.base64_decode)
        base64_buttons.addWidget(self.base64_encode_btn)
        base64_buttons.addWidget(self.base64_decode_btn)
        base64_layout.addLayout(base64_buttons)

        self.base64_output = QPlainTextEdit()
        self.base64_output.setPlaceholderText("待显示编/解码数据...")
        base64_layout.addWidget(self.base64_output)

        # AES Tab
        aes_widget = QWidget()
        aes_layout = QVBoxLayout(aes_widget)
        self.tabWidget.addTab(aes_widget, "AES")

        self.aes_input = QPlainTextEdit()
        self.aes_input.setPlaceholderText("请输入待加/解密的文本数据")
        aes_layout.addWidget(self.aes_input)

        aes_options = QHBoxLayout()
        self.aes_lable_model = QLabel("加密模式")
        self.aes_lable_model.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.aes_lable_model.setFixedWidth(100)
        self.aes_lable_model.setFixedHeight(30)
        self.aes_mode = CustomComboBox()
        self.aes_mode.setFixedHeight(30)
        self.aes_mode.addItems(["CBC", "ECB", "CTR", "OFB", "CFB"])
        self.aes_lable_padding = QLabel("填充方式")
        self.aes_lable_padding.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.aes_lable_padding.setFixedWidth(100)
        self.aes_lable_padding.setFixedHeight(30)
        self.aes_padding = CustomComboBox()
        self.aes_padding.setFixedHeight(30)
        self.aes_padding.addItems(["Pkcs7", "NoPadding", "ZeroPadding", "Iso97971", "AnsiX923", "Iso10126"])
        self.aes_lable_digit = QLabel("位数")
        self.aes_lable_digit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.aes_lable_digit.setFixedWidth(100)
        self.aes_lable_digit.setFixedHeight(30)
        self.aes_digit = CustomComboBox()
        self.aes_digit.setFixedHeight(30)
        self.aes_digit.addItems(["128", "192", "256"])
        aes_options.addWidget(self.aes_lable_model)
        aes_options.addWidget(self.aes_mode)
        aes_options.addWidget(self.aes_lable_padding)
        aes_options.addWidget(self.aes_padding)
        aes_options.addWidget(self.aes_lable_digit)
        aes_options.addWidget(self.aes_digit)
        aes_layout.addLayout(aes_options)

        aes_key_iv = QHBoxLayout()
        self.aes_key = QLineEdit()
        self.aes_key.setPlaceholderText(" 请输入Key值...")
        self.aes_key.setFixedHeight(25)
        self.aes_iv = QLineEdit()
        self.aes_iv.setPlaceholderText(" 请输入IV值...")
        self.aes_iv.setFixedHeight(25)
        aes_key_iv.addWidget(self.aes_key)
        aes_key_iv.addWidget(self.aes_iv)
        aes_layout.addLayout(aes_key_iv)

        aes_buttons = QHBoxLayout()
        self.aes_encrypt_btn = QPushButton("加密")
        self.aes_decrypt_btn = QPushButton("解密")
        self.aes_encrypt_btn.clicked.connect(self.aes_encrypt)
        self.aes_decrypt_btn.clicked.connect(self.aes_decrypt)
        aes_buttons.addWidget(self.aes_encrypt_btn)
        aes_buttons.addWidget(self.aes_decrypt_btn)
        aes_layout.addLayout(aes_buttons)

        self.aes_output = QPlainTextEdit()
        self.aes_output.setPlaceholderText("待显示加/解密数据...")

        aes_options_two = QHBoxLayout()
        self.aes_lable_model_two = QLabel("输入模式")
        self.aes_lable_model_two.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.aes_lable_model_two.setFixedWidth(100)
        self.aes_lable_model_two.setFixedHeight(30)
        self.aes_mode_two = CustomComboBox()
        self.aes_mode_two.addItems(["String", "Base64", "Hex"])
        self.aes_mode_two.setFixedHeight(30)
        self.aes_lable_padding_two = QLabel("输出模式")
        self.aes_lable_padding_two.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.aes_lable_padding_two.setFixedWidth(100)
        self.aes_lable_padding_two.setFixedHeight(30)
        self.aes_padding_two = CustomComboBox()
        self.aes_padding_two.addItems(["Base64", "String", "Hex"])
        self.aes_padding_two.setFixedHeight(30)
        aes_options_two.addWidget(self.aes_lable_model_two)
        aes_options_two.addWidget(self.aes_mode_two)
        aes_options_two.addWidget(self.aes_lable_padding_two)
        aes_options_two.addWidget(self.aes_padding_two)
        aes_layout.addLayout(aes_options_two)

        aes_layout.addWidget(self.aes_output)

        # DES Tab
        des_widget = QWidget()
        des_layout = QVBoxLayout(des_widget)
        self.tabWidget.addTab(des_widget, "DES")

        self.des_input = QPlainTextEdit()
        self.des_input.setPlaceholderText("请输入待加/解密的文本数据")
        des_layout.addWidget(self.des_input)

        des_options = QHBoxLayout()
        self.des_lable_model = QLabel("加密模式")
        self.des_lable_model.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.des_lable_model.setFixedWidth(100)
        self.des_lable_model.setFixedHeight(30)
        self.des_mode = CustomComboBox()
        self.des_mode.setFixedHeight(30)
        self.des_mode.addItems(["CBC", "ECB", "CTR", "OFB", "CFB"])
        self.des_lable_padding = QLabel("填充方式")
        self.des_lable_padding.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.des_lable_padding.setFixedWidth(100)
        self.des_lable_padding.setFixedHeight(30)
        self.des_padding = CustomComboBox()
        self.des_padding.setFixedHeight(30)
        self.des_padding.addItems(["Pkcs7", "NoPadding", "ZeroPadding", "Iso97971", "AnsiX923", "Iso10126"])
        des_options.addWidget(self.des_lable_model)
        des_options.addWidget(self.des_mode)
        des_options.addWidget(self.des_lable_padding)
        des_options.addWidget(self.des_padding)
        des_layout.addLayout(des_options)

        des_key_iv = QHBoxLayout()
        self.des_key = QLineEdit()
        self.des_key.setPlaceholderText(" 请输入Key值...")
        self.des_key.setFixedHeight(25)
        self.des_iv = QLineEdit()
        self.des_iv.setPlaceholderText(" 请输入IV值...")
        self.des_iv.setFixedHeight(25)
        des_key_iv.addWidget(self.des_key)
        des_key_iv.addWidget(self.des_iv)
        des_layout.addLayout(des_key_iv)

        des_buttons = QHBoxLayout()
        self.des_encrypt_btn = QPushButton("加密")
        self.des_decrypt_btn = QPushButton("解密")
        self.des_encrypt_btn.clicked.connect(self.des_encrypt)
        self.des_decrypt_btn.clicked.connect(self.des_decrypt)
        des_buttons.addWidget(self.des_encrypt_btn)
        des_buttons.addWidget(self.des_decrypt_btn)
        des_layout.addLayout(des_buttons)

        self.des_output = QPlainTextEdit()
        self.des_output.setPlaceholderText("待显示加/解密数据...")

        des_options_two = QHBoxLayout()
        self.des_lable_model_two = QLabel("输入模式")
        self.des_lable_model_two.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.des_lable_model_two.setFixedWidth(100)
        self.des_lable_model_two.setFixedHeight(30)
        self.des_mode_two = CustomComboBox()
        self.des_mode_two.addItems(["String", "Base64", "Hex"])
        self.des_mode_two.setFixedHeight(30)
        self.des_lable_padding_two = QLabel("输出模式")
        self.des_lable_padding_two.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.des_lable_padding_two.setFixedWidth(100)
        self.des_lable_padding_two.setFixedHeight(30)
        self.des_padding_two = CustomComboBox()
        self.des_padding_two.addItems(["Base64", "String", "Hex"])
        self.des_padding_two.setFixedHeight(30)
        des_options_two.addWidget(self.des_lable_model_two)
        des_options_two.addWidget(self.des_mode_two)
        des_options_two.addWidget(self.des_lable_padding_two)
        des_options_two.addWidget(self.des_padding_two)
        des_layout.addLayout(des_options_two)

        des_layout.addWidget(self.des_output)

        # RSA Tab
        rsa_widget = QWidget()
        rsa_layout = QVBoxLayout(rsa_widget)
        self.tabWidget.addTab(rsa_widget, "RSA")

        rsa_text = QHBoxLayout()
        self.rsa_password = QPlainTextEdit()
        self.rsa_password.setPlaceholderText("请输入公钥(PEM格式)...")
        self.rsa_text_content = QPlainTextEdit()
        self.rsa_text_content.setPlaceholderText("待加/解密内容...")
        rsa_text.addWidget(self.rsa_password)
        rsa_text.addWidget(self.rsa_text_content)
        rsa_layout.addLayout(rsa_text)

        rsa_options_two = QHBoxLayout()
        self.rsa_lable_model_two = QLabel("输入模式")
        self.rsa_lable_model_two.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rsa_lable_model_two.setFixedWidth(100)
        self.rsa_lable_model_two.setFixedHeight(30)
        self.rsa_mode_two = CustomComboBox()
        self.rsa_mode_two.addItems(["String", "Base64", "Hex"])
        self.rsa_mode_two.setFixedHeight(30)
        self.rsa_lable_padding_two = QLabel("输出模式")
        self.rsa_lable_padding_two.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rsa_lable_padding_two.setFixedWidth(100)
        self.rsa_lable_padding_two.setFixedHeight(30)
        self.rsa_padding_two = CustomComboBox()
        self.rsa_padding_two.addItems(["Base64", "String", "Hex"])
        self.rsa_padding_two.setFixedHeight(30)
        rsa_options_two.addWidget(self.rsa_lable_model_two)
        rsa_options_two.addWidget(self.rsa_mode_two)
        rsa_options_two.addWidget(self.rsa_lable_padding_two)
        rsa_options_two.addWidget(self.rsa_padding_two)
        rsa_layout.addLayout(rsa_options_two)

        rsa_options = QHBoxLayout()
        self.rsa_encrypt_btn = QPushButton("加密")
        self.rsa_decrypt_btn = QPushButton("解密")
        self.rsa_encrypt_btn.clicked.connect(self.rsa_encrypt)
        self.rsa_decrypt_btn.clicked.connect(self.rsa_decrypt)
        rsa_options.addWidget(self.rsa_encrypt_btn)
        rsa_options.addWidget(self.rsa_decrypt_btn)
        rsa_layout.addLayout(rsa_options)

        self.rsa_result = QPlainTextEdit()
        self.rsa_result.setPlaceholderText("待显示加/解密数据...")
        rsa_layout.addWidget(self.rsa_result)

        # HMAC Tab
        hmac_widget = QWidget()
        hmac_layout = QVBoxLayout(hmac_widget)
        self.tabWidget.addTab(hmac_widget, "HMAC")

        self.hmac_text = QPlainTextEdit()
        self.hmac_text.setPlaceholderText("请输入待HMAC处理的文本数据...")
        self.hmac_text.setFixedHeight(200)
        hmac_layout.addWidget(self.hmac_text)

        hmac_options = QHBoxLayout()
        self.hmac_type = QLabel("文本格式")
        self.hmac_type.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hmac_type.setFixedWidth(100)
        self.hmac_type.setFixedHeight(30)
        self.hmac_mode = CustomComboBox()
        self.hmac_mode.addItems(["String", "Base64", "HEX"])
        self.hmac_mode.setFixedHeight(30)
        self.hmac_key = QLineEdit()
        self.hmac_key.setPlaceholderText(" 请输入Key值...")
        self.hmac_key.setFixedHeight(25)
        hmac_options.addWidget(self.hmac_type)
        hmac_options.addWidget(self.hmac_mode)
        hmac_options.addWidget(self.hmac_key)
        hmac_layout.addLayout(hmac_options)

        hmac_result = QHBoxLayout()
        self.hmac_md5 = QPlainTextEdit()
        self.hmac_md5.setPlaceholderText("HMAC-MD5值...")
        self.hmac_sha1 = QPlainTextEdit()
        self.hmac_sha1.setPlaceholderText("HMAC-SHA1值...")
        hmac_result.addWidget(self.hmac_md5)
        hmac_result.addWidget(self.hmac_sha1)
        hmac_layout.addLayout(hmac_result)
        self.hmac_text.textChanged.connect(self.calculate_hmac)
        self.hmac_key.textChanged.connect(self.calculate_hmac)
        self.hmac_mode.currentIndexChanged.connect(self.calculate_hmac)

        hmac_result2 = QHBoxLayout()
        self.hmac_sha256 = QPlainTextEdit()
        self.hmac_sha256.setPlaceholderText("HMAC-SHA256值...")
        self.hmac_sha512 = QPlainTextEdit()
        self.hmac_sha512.setPlaceholderText("HMAC-SHA512值...")
        hmac_result2.addWidget(self.hmac_sha256)
        hmac_result2.addWidget(self.hmac_sha512)
        hmac_layout.addLayout(hmac_result2)

        # DES3 Tab
        des3_widget = QWidget()
        des3_layout = QVBoxLayout(des3_widget)
        self.tabWidget.addTab(des3_widget, "3DES")

        self.des3_input = QPlainTextEdit()
        self.des3_input.setPlaceholderText("请输入待加/解密的文本数据")
        des3_layout.addWidget(self.des3_input)

        des3_options = QHBoxLayout()
        self.des3_lable_model = QLabel("加密模式")
        self.des3_lable_model.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.des3_lable_model.setFixedWidth(100)
        self.des3_lable_model.setFixedHeight(30)
        self.des3_mode = CustomComboBox()
        self.des3_mode.setFixedHeight(30)
        self.des3_mode.addItems(["CBC", "ECB", "CTR", "OFB", "CFB"])
        self.des3_lable_padding = QLabel("填充方式")
        self.des3_lable_padding.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.des3_lable_padding.setFixedWidth(100)
        self.des3_lable_padding.setFixedHeight(30)
        self.des3_padding = CustomComboBox()
        self.des3_padding.setFixedHeight(30)
        self.des3_padding.addItems(["Pkcs7", "NoPadding", "ZeroPadding", "Iso97971", "AnsiX923", "Iso10126"])
        des3_options.addWidget(self.des3_lable_model)
        des3_options.addWidget(self.des3_mode)
        des3_options.addWidget(self.des3_lable_padding)
        des3_options.addWidget(self.des3_padding)
        des3_layout.addLayout(des3_options)

        des3_key_iv = QHBoxLayout()
        self.des3_key = QLineEdit()
        self.des3_key.setPlaceholderText(" 请输入Key值...")
        self.des3_key.setFixedHeight(25)
        self.des3_iv = QLineEdit()
        self.des3_iv.setPlaceholderText(" 请输入IV值...")
        self.des3_iv.setFixedHeight(25)
        des3_key_iv.addWidget(self.des3_key)
        des3_key_iv.addWidget(self.des3_iv)
        des3_layout.addLayout(des3_key_iv)

        des3_buttons = QHBoxLayout()
        self.des3_encrypt_btn = QPushButton("加密")
        self.des3_decrypt_btn = QPushButton("解密")
        self.des3_encrypt_btn.clicked.connect(self.des3_encrypt)
        self.des3_decrypt_btn.clicked.connect(self.des3_decrypt)
        des3_buttons.addWidget(self.des3_encrypt_btn)
        des3_buttons.addWidget(self.des3_decrypt_btn)
        des3_layout.addLayout(des3_buttons)

        self.des3_output = QPlainTextEdit()
        self.des3_output.setPlaceholderText("待显示加/解密数据...")

        des3_options_two = QHBoxLayout()
        self.des3_lable_model_two = QLabel("输入模式")
        self.des3_lable_model_two.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.des3_lable_model_two.setFixedWidth(100)
        self.des3_lable_model_two.setFixedHeight(30)
        self.des3_mode_two = CustomComboBox()
        self.des3_mode_two.addItems(["String", "Base64", "Hex"])
        self.des3_mode_two.setFixedHeight(30)
        self.des3_lable_padding_two = QLabel("输出模式")
        self.des3_lable_padding_two.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.des3_lable_padding_two.setFixedWidth(100)
        self.des3_lable_padding_two.setFixedHeight(30)
        self.des3_padding_two = CustomComboBox()
        self.des3_padding_two.addItems(["Base64", "String", "Hex"])
        self.des3_padding_two.setFixedHeight(30)
        des3_options_two.addWidget(self.des3_lable_model_two)
        des3_options_two.addWidget(self.des3_mode_two)
        des3_options_two.addWidget(self.des3_lable_padding_two)
        des3_options_two.addWidget(self.des3_padding_two)
        des3_layout.addLayout(des3_options_two)

        des3_layout.addWidget(self.des3_output)

        # Unicode Tab
        unicode_widget = QWidget()
        unicode_layout = QVBoxLayout(unicode_widget)
        self.tabWidget.addTab(unicode_widget, "Unicode")

        self.unicode_input = QPlainTextEdit()
        self.unicode_input.setPlaceholderText("请输入待编/解码的文本数据")
        unicode_layout.addWidget(self.unicode_input)

        unicode_buttons = QHBoxLayout()
        self.unicode_encode_btn = QPushButton("编码")
        self.unicode_decode_btn = QPushButton("解码")
        unicode_buttons.addWidget(self.unicode_encode_btn)
        unicode_buttons.addWidget(self.unicode_decode_btn)
        self.unicode_encode_btn.clicked.connect(self.unicode_encode)
        self.unicode_decode_btn.clicked.connect(self.unicode_decode)
        unicode_layout.addLayout(unicode_buttons)

        self.unicode_output = QPlainTextEdit()
        self.unicode_output.setPlaceholderText("待显示编/解码数据...")
        unicode_layout.addWidget(self.unicode_output)

        # JWT Tab
        jwt_widget = QWidget()
        jwt_layout = QVBoxLayout(jwt_widget)
        self.tabWidget.addTab(jwt_widget, "JWT")

        self.jwt_input = QPlainTextEdit()
        self.jwt_input.setPlaceholderText("请输入待编/解码的JWT数据")
        jwt_layout.addWidget(self.jwt_input)

        jwt_buttons = QHBoxLayout()
        self.jwt_key = QLineEdit()
        self.jwt_key.setFixedWidth(200)
        self.jwt_key.setPlaceholderText(" 请输入Key值...")
        self.jwt_key.setFixedHeight(25)
        self.jwt_encode_btn = QPushButton("编码")
        self.jwt_decode_btn = QPushButton("解码")
        self.jwt_encode_btn.clicked.connect(self.jwt_encode)
        self.jwt_decode_btn.clicked.connect(self.jwt_decode)
        jwt_buttons.addWidget(self.jwt_key)
        jwt_buttons.addWidget(self.jwt_encode_btn)
        jwt_buttons.addWidget(self.jwt_decode_btn)
        jwt_layout.addLayout(jwt_buttons)

        self.jwt_output = QPlainTextEdit()
        self.jwt_output.setPlaceholderText("待显示编/解码数据...")
        jwt_layout.addWidget(self.jwt_output)

        # StringHex Tab
        stringhex_widget = QWidget()
        stringhex_layout = QVBoxLayout(stringhex_widget)
        self.tabWidget.addTab(stringhex_widget, "String/Hex")

        self.stringhex_input = QPlainTextEdit()
        self.stringhex_input.setPlaceholderText("请输入待转换的文本数据")
        stringhex_layout.addWidget(self.stringhex_input)

        stringhex_buttons = QHBoxLayout()
        self.stringhex_encode_btn = QPushButton("String -> Hex")
        self.stringhex_decode_btn = QPushButton("Hex -> String")
        stringhex_buttons.addWidget(self.stringhex_encode_btn)
        stringhex_buttons.addWidget(self.stringhex_decode_btn)
        self.stringhex_encode_btn.clicked.connect(self.string_to_hex)
        self.stringhex_decode_btn.clicked.connect(self.hex_to_string)

        stringhex_layout.addLayout(stringhex_buttons)

        self.stringhex_output = QPlainTextEdit()
        self.stringhex_output.setPlaceholderText("待显示转换后的数据内容...")
        stringhex_layout.addWidget(self.stringhex_output)

        self.setLayout(main_layout)
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
                    height: 25px;
                    border-radius: 5px;
                }

                QPushButton:hover {
                    background-color: #3366CC;
                    color: white;
                }
            """)

    def update_hashes(self):
        input_text = self.textEdit.toPlainText()
        is_uppercase = self.checkBox.isChecked()
        hashes = ef.update_hashes(input_text, is_uppercase)
        for hash_type, hash_value in hashes.items():
            self.hash_results[hash_type].setPlainText(hash_value)

    def url_encode(self):
        url_input = self.url_input.toPlainText()
        encoded_url = ef.url_encode(url_input)
        self.url_output.setPlainText(encoded_url)

    def url_decode(self):
        input_text = self.url_input.toPlainText()
        decoded_text = ef.url_decode(input_text)
        self.url_output.setPlainText(decoded_text)

    def base64_encode(self):
        input_text = self.base64_input.toPlainText()
        encoded_text = ef.base64_encode(input_text)
        self.base64_output.setPlainText(encoded_text)

    def base64_decode(self):
        input_text = self.base64_input.toPlainText()
        decoded_text = ef.base64_decode(input_text)
        self.base64_output.setPlainText(decoded_text)

    def aes_encrypt(self):
        mode = self.aes_mode.currentText()
        padding = self.aes_padding.currentText()
        key = self.aes_key.text().encode()
        iv = self.aes_iv.text().encode()
        data = self.aes_input.toPlainText()
        key_size = int(self.aes_digit.currentText())
        input_mode = self.aes_mode_two.currentText()
        output_mode = self.aes_padding_two.currentText()
        encrypted_data = ef.aes_encrypt(mode, padding, key, iv, data, key_size, input_mode, output_mode)
        self.aes_output.setPlainText(encrypted_data)

    def aes_decrypt(self):
        mode = self.aes_mode.currentText()
        padding = self.aes_padding.currentText()
        key = self.aes_key.text().encode()
        iv = self.aes_iv.text().encode()
        data = self.aes_input.toPlainText()
        key_size = int(self.aes_digit.currentText())
        input_mode = self.aes_mode_two.currentText()
        output_mode = self.aes_padding_two.currentText()
        decrypted_data = ef.aes_decrypt(mode, padding, key, iv, data, key_size, input_mode, output_mode)
        self.aes_output.setPlainText(decrypted_data)

    def des_decrypt(self):
        mode = self.des_mode.currentText()
        padding = self.des_padding.currentText()
        key = self.des_key.text().encode()
        iv = self.des_iv.text().encode()
        data = self.des_input.toPlainText()
        input_mode = self.des_mode_two.currentText()
        output_mode = self.des_padding_two.currentText()
        decrypted_data = ef.des_decrypt(mode, padding, key, iv, data, input_mode, output_mode)
        self.des_output.setPlainText(decrypted_data)

    def des_encrypt(self):
        mode = self.des_mode.currentText()
        padding = self.des_padding.currentText()
        key = self.des_key.text().encode()
        iv = self.des_iv.text().encode()
        data = self.des_input.toPlainText()
        input_mode = self.des_mode_two.currentText()
        output_mode = self.des_padding_two.currentText()
        decrypted_data = ef.des_encrypt(mode, padding, key, iv, data, input_mode, output_mode)
        self.des_output.setPlainText(decrypted_data)

    def rsa_encrypt(self):
        rsa_password = self.rsa_password.toPlainText()
        input_mode = self.rsa_mode_two.currentText()
        data = self.rsa_text_content.toPlainText()
        output_mode = self.rsa_padding_two.currentText()
        encrypt_data = ef.rsa_encrypt(rsa_password, input_mode, data, output_mode)
        self.rsa_result.setPlainText(encrypt_data)

    def rsa_decrypt(self):
        rsa_password = self.rsa_password.toPlainText()
        input_mode = self.rsa_mode_two.currentText()
        data = self.rsa_text_content.toPlainText()
        output_mode = self.rsa_padding_two.currentText()
        encrypt_data = ef.rsa_decrypt(rsa_password, input_mode, data, output_mode)
        self.rsa_result.setPlainText(encrypt_data)

    def calculate_hmac(self):
        text = self.hmac_text.toPlainText()
        key = self.hmac_key.text().encode()
        mode = self.hmac_mode.currentText()
        md5, sha1, sha256, sha512 = ef.calculate_hmac(text, key, mode)
        self.hmac_md5.setPlainText(md5)
        self.hmac_sha1.setPlainText(sha1)
        self.hmac_sha256.setPlainText(sha256)
        self.hmac_sha512.setPlainText(sha512)

    def des3_decrypt(self):
        mode = self.des3_mode.currentText()
        padding = self.des3_padding.currentText()
        key = self.des3_key.text().encode()
        iv = self.des3_iv.text().encode()
        data = self.des3_input.toPlainText()
        input_mode = self.des3_mode_two.currentText()
        output_mode = self.des3_padding_two.currentText()
        decrypted_data = ef.des3_decrypt(mode, padding, key, iv, data, input_mode, output_mode)
        self.des3_output.setPlainText(decrypted_data)

    def des3_encrypt(self):
        mode = self.des3_mode.currentText()
        padding = self.des3_padding.currentText()
        key = self.des3_key.text().encode()
        iv = self.des3_iv.text().encode()
        data = self.des3_input.toPlainText()
        input_mode = self.des3_mode_two.currentText()
        output_mode = self.des3_padding_two.currentText()
        decrypted_data = ef.des3_encrypt(mode, padding, key, iv, data, input_mode, output_mode)
        self.des3_output.setPlainText(decrypted_data)

    def unicode_encode(self):
        data = self.unicode_input.toPlainText()
        encoded_data = ef.unicode_encode(data)
        self.unicode_output.setPlainText(encoded_data)

    def unicode_decode(self):
        data = self.unicode_input.toPlainText()
        decoded_data = ef.unicode_decode(data)
        self.unicode_output.setPlainText(decoded_data)

    def jwt_encode(self):
        data = self.jwt_input.toPlainText()
        key = self.jwt_key.text()
        encoded_data = ef.jwt_encode(data, key)
        self.jwt_output.setPlainText(encoded_data)

    def jwt_decode(self):
        data = self.jwt_input.toPlainText()
        key = self.jwt_key.text()
        decoded_data = ef.jwt_decode(data, key)
        self.jwt_output.setPlainText(decoded_data)

    def string_to_hex(self):
        data = self.stringhex_input.toPlainText()
        hex_data = ef.string_to_hex(data)
        self.stringhex_output.setPlainText(hex_data)

    def hex_to_string(self):
        data = self.stringhex_input.toPlainText()
        string_data = ef.hex_to_string(data)
        self.stringhex_output.setPlainText(string_data)