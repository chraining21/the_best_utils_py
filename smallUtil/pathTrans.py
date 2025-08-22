import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QApplication
import qtawesome as qta

class PathTransTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('輸入路徑...')
        self.layout.addWidget(self.input_field)

        self.convert_button = QPushButton('轉換成windows格式並複製')
        self.convert_button.clicked.connect(self.convert_and_copy_windows)
        self.layout.addWidget(self.convert_button)
        
        self.convert_button = QPushButton('轉換成linux格式並複製')
        self.convert_button.clicked.connect(self.convert_and_copy_linux)
        self.layout.addWidget(self.convert_button)
        
        self.convert_button = QPushButton('Windows轉換成linux格式並複製')
        self.convert_button.clicked.connect(self.convert_windows_and_copy_linux)
        self.layout.addWidget(self.convert_button)

        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        self.layout.addWidget(self.output_field)

    def convert_and_copy_windows(self):
        input_text = self.input_field.text()
        converted_text = input_text.replace('.', '\\')
        self.output_field.setText('\\'+converted_text)

        # 複製到剪貼板
        clipboard = QApplication.clipboard()
        clipboard.setText('\\'+converted_text)
    def convert_and_copy_linux(self):
        input_text = self.input_field.text()
        converted_text = input_text.replace('.', '/')
        self.output_field.setText('/'+converted_text)

        # 複製到剪貼板
        clipboard = QApplication.clipboard()
        clipboard.setText('/'+converted_text)
    def convert_windows_and_copy_linux(self):
        input_text = self.input_field.text()
        converted_text = input_text.replace('\\', '/')
        self.output_field.setText('/'+converted_text)

        # 複製到剪貼板
        clipboard = QApplication.clipboard()
        clipboard.setText('/'+converted_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PathTransTab()
    window.show()
    sys.exit(app.exec_())
