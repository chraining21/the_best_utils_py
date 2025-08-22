import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QApplication
import qtawesome as qta

class StringTrans(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('輸入...')
        self.layout.addWidget(self.input_field)

        self.convert_button = QPushButton('轉換成大寫空白')
        self.convert_button.clicked.connect(self.convert_camel_case)
        self.layout.addWidget(self.convert_button)
        
        self.convert_button = QPushButton('轉換成API DOC')
        self.convert_button.clicked.connect(self.conver_api_doc)
        self.layout.addWidget(self.convert_button)
        
        
        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        self.layout.addWidget(self.output_field)

    def convert_camel_case(self):
        text = self.input_field.text()
        words = []
        current_word = ""
        for char in text:
            if char.isupper() and current_word:
                words.append(current_word)
                current_word = ""
            current_word += char
        if current_word:
            words.append(current_word)
        converted_text =" ".join(word.capitalize() for word in words)
        self.output_field.setText(converted_text)
        # 複製到剪貼板
        clipboard = QApplication.clipboard()
        clipboard.setText(converted_text)
        
    def conver_api_doc(self):
        text = self.input_field.text()
        lines = text.strip().split("\n")
        variable_names = []

        for line in lines:
            # 去除行首尾空白字符
            line = line.strip()
            
            # 檢查是否包含 'transient'，如果有則跳過
            if "transient" in line:
                continue
            
            # 拆分字符串，獲取最後一個單詞（變量名稱）
            parts = line.split()
            if parts:  # 確保行不為空
                variable_name = parts[-1].strip(";")  # 去除行尾的分號
                variable_names.append(variable_name)
        converted_text ="\n".join(variable_names)
        self.output_field.setText(converted_text)
        # 複製到剪貼板
        clipboard = QApplication.clipboard()
        clipboard.setText(converted_text)
      
 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StringTrans()
    window.show()
    sys.exit(app.exec_())
