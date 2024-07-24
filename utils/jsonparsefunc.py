import json
from PyQt6.QtWidgets import QMessageBox, QTreeWidgetItem
from PyQt6.QtCore import Qt

def format_json(input_text):
    try:
        json_data = json.loads(input_text.toPlainText())
        formatted_json = json.dumps(json_data, indent=4, ensure_ascii=False)
        input_text.setPlainText(formatted_json)
    except json.JSONDecodeError as e:
        show_error_message(f"无效的JSON: {e}")

def unescape_json(input_text):
    try:
        json_data = json.loads(input_text.toPlainText())
        unescaped_json = json.dumps(json_data, ensure_ascii=False)
        input_text.setPlainText(unescaped_json)
    except json.JSONDecodeError as e:
        show_error_message(f"无效的JSON: {e}")

def parse_to_tree(input_text, show_tree):
    try:
        json_data = json.loads(input_text.toPlainText())
        show_tree.clear()
        add_items(show_tree.invisibleRootItem(), json_data)
    except json.JSONDecodeError as e:
        show_error_message(f"无效的JSON: {e}")

def add_items(parent, value, path=""):
    if isinstance(value, dict):
        for key, val in value.items():
            item = QTreeWidgetItem([key])
            new_path = f"{path}['{key}']"
            item.setData(0, Qt.ItemDataRole.UserRole, new_path)
            parent.addChild(item)
            add_items(item, val, new_path)
    elif isinstance(value, list):
        for index, val in enumerate(value):
            item = QTreeWidgetItem([str(index)])
            new_path = f"{path}[{index}]"
            item.setData(0, Qt.ItemDataRole.UserRole, new_path)
            parent.addChild(item)
            add_items(item, val, new_path)
    else:
        item = QTreeWidgetItem([str(value)])
        item.setData(0, Qt.ItemDataRole.UserRole, path)
        parent.addChild(item)

def show_error_message(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle("提示信息")
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.setStyleSheet("")
    msg_box.exec()