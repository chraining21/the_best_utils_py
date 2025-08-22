import os
import sys
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QLabel

class BatchCommandTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 創建存儲指令的列表
        self.commands = []

        # 輸入框和按鈕區域
        self.input_layout = QHBoxLayout()
        self.layout.addLayout(self.input_layout)

        self.command_label = QLabel('輸入批次命令:')
        self.input_layout.addWidget(self.command_label)

        self.command_input = QLineEdit()
        self.input_layout.addWidget(self.command_input)

        self.save_button = QPushButton('保存命令')
        self.save_button.clicked.connect(self.save_command)
        self.input_layout.addWidget(self.save_button)

        # 顯示和執行指令區域
        self.commands_layout = QVBoxLayout()
        self.layout.addLayout(self.commands_layout)

        self.execute_button = QPushButton('執行所有命令')
        self.execute_button.clicked.connect(self.execute_commands)
        self.layout.addWidget(self.execute_button)

        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        self.layout.addWidget(self.output_field)

    def save_command(self):
        command = self.command_input.text()
        if command:
            self.commands.append(command)
            command_label = QLabel(command)
            self.commands_layout.addWidget(command_label)
            self.command_input.clear()

    def execute_commands(self):
        for command in self.commands:
            self.output_field.append(f"執行: {command}")
            result = os.popen(command).read()
            self.output_field.append(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BatchCommandTab()
    window.show()
    sys.exit(app.exec_())
