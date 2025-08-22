import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QMessageBox, QApplication

class TextComparerTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 输入文本区域
        self.input1_label = QLabel('文本1:')
        self.layout.addWidget(self.input1_label)

        self.input1_field = QTextEdit()
        self.layout.addWidget(self.input1_field)

        self.input2_label = QLabel('文本2:')
        self.layout.addWidget(self.input2_label)

        self.input2_field = QTextEdit()
        self.layout.addWidget(self.input2_field)

        # 对比按钮
        self.compare_button = QPushButton('對比文本')
        self.compare_button.clicked.connect(self.compare_texts)
        self.layout.addWidget(self.compare_button)

        # 结果显示区域
        self.result_label = QLabel('差異:')
        self.layout.addWidget(self.result_label)

        self.result_field = QTextEdit()
        self.result_field.setReadOnly(True)
        self.layout.addWidget(self.result_field)

    def compare_texts(self):
        text1 = self.input1_field.toPlainText().splitlines()
        text2 = self.input2_field.toPlainText().splitlines()

        diff_result = []
        for i, (line1, line2) in enumerate(zip(text1, text2), start=1):
            if line1 != line2:
                diff_result.append(f'Line {i}:\n- {line1}\n+ {line2}\n')

        # 如果文件1有多余的行
        if len(text1) > len(text2):
            for i in range(len(text2), len(text1)):
                diff_result.append(f'Line {i+1}:\n- {text1[i]}\n')

        # 如果文件2有多余的行
        if len(text2) > len(text1):
            for i in range(len(text1), len(text2)):
                diff_result.append(f'Line {i+1}:\n+ {text2[i]}\n')

        if not diff_result:
            self.result_field.setText('文本没有差异')
        else:
            self.result_field.setText('\n'.join(diff_result))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextComparerTab()
    window.show()
    sys.exit(app.exec_())
