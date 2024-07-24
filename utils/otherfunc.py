from PyQt6.QtCore import QTimer
from datetime import datetime
from pypinyin import pinyin, Style
import random
import uuid
from difflib import ndiff
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor

def start_timer(self):
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.update_time)
    self.timer.start(1000)

def convert_to_pinyin(self):
    text = self.pinyin_input.text()
    pinyin_list = pinyin(text, heteronym=False)
    formatted_pinyin = ' '.join(word[0] for word in pinyin_list)
    self.pinyin_result_text.setText(formatted_pinyin)

def generate_random_strings(self):
    try:
        characters = self.random_result_setting.toPlainText()
        num_strings = int(self.random_sum.text())
        length_strings = int(self.random_sum_length.text())
        self.random_result_text.clear()
        results = []
        for i in range(num_strings):
            random_string = ''.join(random.choice(characters) for _ in range(length_strings))
            if i == num_strings - 1:
                results.append(random_string)
            else:
                results.append(random_string + ",\n")
        self.random_result_text.setPlainText(''.join(results))
    except:
        pass

def generate_uuids(self):
    count = int(self.uuid_sum.text()) if self.uuid_sum.text().isdigit() else 0
    uuids = [str(uuid.uuid4()) for _ in range(count)]
    formatted_result = ",\n".join(uuids)
    self.uuid_result_text.setPlainText(formatted_result)

def compare_texts(self):
    try:
        self.text_comparison_text.blockSignals(True)
        self.text_comparison_result.blockSignals(True)
        original_text = self.text_comparison_text.toPlainText()
        compared_text = self.text_comparison_result.toPlainText()
        highlight_differences(self, original_text, compared_text)
        self.text_comparison_text.blockSignals(False)
        self.text_comparison_result.blockSignals(False)
    except Exception as e:
        print(e)
        pass

def highlight_differences(self, original, compared):
    reset_formatting(self, self.text_comparison_text)
    reset_formatting(self, self.text_comparison_result)

    diff = ndiff(original.splitlines(keepends=True), compared.splitlines(keepends=True))
    original_cursor = QTextCursor(self.text_comparison_text.document())
    compared_cursor = QTextCursor(self.text_comparison_result.document())

    yellow_background = QTextCharFormat()
    yellow_background.setBackground(QColor('yellow'))

    for line in diff:
        if line.startswith('+ '):
            apply_format(self, compared_cursor, line[2:], yellow_background)
        elif line.startswith('- '):
            apply_format(self, original_cursor, line[2:], yellow_background)

def reset_formatting(self, text_edit):
    cursor = QTextCursor(text_edit.document())
    cursor.select(QTextCursor.SelectionType.Document)
    cursor.setCharFormat(QTextCharFormat())
    cursor.clearSelection()

def apply_format(self, cursor, text, format):
    pos = cursor.document().toPlainText().find(text)
    if pos != -1:
        cursor.setPosition(pos)
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, len(text))
        cursor.mergeCharFormat(format)