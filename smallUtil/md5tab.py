import hashlib
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout,QApplication

class MD5Tab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.input_labels = []
        self.text_inputs = []
        self.create_input_fields(5)  # 创建5个输入字段，可以根据需要调整数量

        self.hash_button = QPushButton('计算 MD5')
        self.hash_button.clicked.connect(self.calculate_md5)
        self.layout.addWidget(self.hash_button)

        self.result_label = QLabel('MD5 哈希值：')
        self.layout.addWidget(self.result_label)

        self.hash_result = QLineEdit()
        self.hash_result.setReadOnly(True)
        self.layout.addWidget(self.hash_result)

    def create_input_fields(self, num_fields):
        for i in range(num_fields):
            hbox = QHBoxLayout()
            label = QLabel(f'输入文本 {i+1}：')
            hbox.addWidget(label)
            self.layout.addLayout(hbox)
            self.input_labels.append(label)

            text_input = QLineEdit()
            hbox.addWidget(text_input)
            self.layout.addLayout(hbox)
            self.text_inputs.append(text_input)

    def calculate_md5(self):
        combined_text = ''.join([text_input.text() for text_input in self.text_inputs])
        md5_hash = hashlib.md5(combined_text.encode('utf-8')).hexdigest()
        self.hash_result.setText(md5_hash)
        #複製
        clipboard = QApplication.clipboard()
        clipboard.setText(md5_hash)

