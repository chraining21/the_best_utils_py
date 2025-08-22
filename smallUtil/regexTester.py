import re
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QMessageBox, QHBoxLayout

class RegexTesterTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 输入字符串区域
        self.input_label = QLabel('輸入字符串:')
        self.layout.addWidget(self.input_label)

        self.input_field = QTextEdit()
        self.layout.addWidget(self.input_field)

        # 输入正则表达式区域
        self.regex_label = QLabel('輸入正則表達式:')
        self.layout.addWidget(self.regex_label)

        self.regex_input = QLineEdit()
        self.layout.addWidget(self.regex_input)

        # 测试按钮
        self.test_button = QPushButton('測試正則表達式')
        self.test_button.clicked.connect(self.test_regex)
        self.layout.addWidget(self.test_button)

        # 匹配结果显示区域
        self.result_label = QLabel('匹配結果:')
        self.layout.addWidget(self.result_label)

        self.result_field = QTextEdit()
        self.result_field.setReadOnly(True)
        self.layout.addWidget(self.result_field)

        # 常用正则表达式示例区域
        self.examples_label = QLabel('常用正則表達式示例:')
        self.layout.addWidget(self.examples_label)

        self.examples_field = QTextEdit()
        self.examples_field.setReadOnly(True)
        self.layout.addWidget(self.examples_field)
        self.load_examples()

    def test_regex(self):
        input_text = self.input_field.toPlainText()
        regex_pattern = self.regex_input.text()

        try:
            matches = re.findall(regex_pattern, input_text)
            if matches:
                self.result_field.setText('\n'.join(matches))
            else:
                self.result_field.setText('無匹配結果')
        except re.error as e:
            QMessageBox.critical(self, '錯誤', f'正則表達式錯誤: {e}')

    def load_examples(self):
        examples = """
        ^hello: 匹配以hello开头的字符串
        \d+: 匹配一个或多个数字
        \w+: 匹配一个或多个字母、数字或下划线
        [a-z]+: 匹配一个或多个小写字母
        [A-Z]+: 匹配一个或多个大写字母
        [a-zA-Z]+: 匹配一个或多个大小写字母
        \s: 匹配一个空白字符
        \S: 匹配一个非空白字符
        \bword\b: 匹配整个单词word
        ^start: 匹配以start开头的字符串
        end$: 匹配以end结尾的字符串
        .: 匹配任意字符
        (abc|def): 匹配abc或def
        """
        self.examples_field.setText(examples)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegexTesterTab()
    window.show()
    sys.exit(app.exec_())
