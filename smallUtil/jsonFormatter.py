import json
import sys
from PyQt5.QtWidgets import  QWidget, QVBoxLayout, QPushButton, QTextEdit, QMessageBox, QApplication
import qtawesome as qta

class JsonFormatterTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText('輸入 JSON 字符串...')
        self.layout.addWidget(self.input_field)

        self.format_button = QPushButton('格式化 JSON')
        self.format_button.setIcon(qta.icon('fa5s.keyboard'))
        self.format_button.clicked.connect(self.format_json)
        self.layout.addWidget(self.format_button)
        
        self.format_button = QPushButton('壓縮 JSON')
        self.format_button.setIcon(qta.icon('fa5s.keyboard'))
        self.format_button.clicked.connect(self.compress_json)
        self.layout.addWidget(self.format_button)

        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        self.layout.addWidget(self.output_field)

    def format_json(self):
        try:
            input_text = self.input_field.toPlainText()
            json_object = json.loads(input_text)
            formatted_json = json.dumps(json_object, indent=4, ensure_ascii=False)
            self.output_field.setText(formatted_json)
            clipboard = QApplication.clipboard()
            clipboard.setText(formatted_json)
        except json.JSONDecodeError:
            QMessageBox.critical(self, '錯誤', '輸入的不是有效的 JSON 字符串')
            
    def compress_json(self):
        try:
            input_text = self.input_field.toPlainText()
            json_object = json.loads(input_text)
            compressed_json = json.dumps(json_object, separators=(',', ':'), ensure_ascii=False)
            self.output_field.setText(compressed_json)
            clipboard = QApplication.clipboard()
            clipboard.setText(compressed_json)
        except json.JSONDecodeError:
            QMessageBox.critical(self, '錯誤', '輸入的不是有效的 JSON 字符串')


