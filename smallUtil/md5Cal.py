import hashlib
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QApplication,QTextEdit
import qtawesome as qta
class MD5Cal(QWidget):
    def __init__(self):
        super().__init__()  
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.text_area = QTextEdit()  # 创建多行文本输入框
        self.text_area.setPlaceholderText('輸入值...')
        self.layout.addWidget(self.text_area)

        self.secret_key_input = QLineEdit()  # 创建Secret Key的单行输入框
        self.secret_key_input.setPlaceholderText('輸入Secret Key...')
        self.layout.addWidget(self.secret_key_input)

        self.hash_button = QPushButton('輸出並複製')
        self.hash_button.setIcon(qta.icon('fa5s.user-secret'))
        self.hash_button.clicked.connect(self.calculate_md5)
        self.layout.addWidget(self.hash_button)

        self.hash_result = QLineEdit()
        self.hash_result.setReadOnly(True)
        self.layout.addWidget(self.hash_result)

    def calculate_md5(self):
        combined_text = ''
        input_text = self.text_area.toPlainText()  # 获取多行文本输入框的内容

        for line in input_text.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)  # 按照 ':' 分割字符串，最多分割一次
                combined_text += value.strip()  # 去除空格后，拼接值

        secret_key = self.secret_key_input.text().strip()  # 获取Secret Key的值
        combined_text += secret_key  # 将Secret Key加到拼接字符串的末尾

        md5_hash = hashlib.md5(combined_text.encode('utf-8')).hexdigest()
        self.hash_result.setText(md5_hash)

        # 复制到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(md5_hash)


# 测试代码
if __name__ == '__main__':
    app = QApplication([])
    window = MD5Cal()
    window.show()
    app.exec_()
