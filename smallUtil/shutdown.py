import sys
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout, QMessageBox, QApplication

class ShutdownTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 創建時間輸入框
        self.time_layout = QHBoxLayout()
        self.layout.addLayout(self.time_layout)

        self.hour_input = QLineEdit()
        self.hour_input.setPlaceholderText('時')
        self.time_layout.addWidget(self.hour_input)

        self.minute_input = QLineEdit()
        self.minute_input.setPlaceholderText('分')
        self.time_layout.addWidget(self.minute_input)

        self.second_input = QLineEdit()
        self.second_input.setPlaceholderText('秒')
        self.time_layout.addWidget(self.second_input)

        # 創建休眠按鈕
        self.hibernate_button = QPushButton('休眠')
        self.hibernate_button.clicked.connect(self.confirm_hibernate)
        self.layout.addWidget(self.hibernate_button)

        # 創建關機按鈕
        self.shutdown_button = QPushButton('關機')
        self.shutdown_button.clicked.connect(self.confirm_shutdown)
        self.layout.addWidget(self.shutdown_button)

        # 創建取消按鈕
        self.cancel_button = QPushButton('取消')
        self.cancel_button.clicked.connect(self.cancel_action)
        self.layout.addWidget(self.cancel_button)

    def confirm_hibernate(self):
        reply = QMessageBox.question(self, '確認', '確定要休眠嗎？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.hibernate()

    def confirm_shutdown(self):
        reply = QMessageBox.question(self, '確認', '確定要關機嗎？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.schedule_shutdown()

    def hibernate(self):
        if sys.platform == 'win32':
            os.system('shutdown /h')
        elif sys.platform == 'linux' or sys.platform == 'darwin':
            os.system('systemctl suspend')

    def schedule_shutdown(self):
        hours = self.hour_input.text()
        minutes = self.minute_input.text()
        seconds = self.second_input.text()

        try:
            hours = int(hours) if hours else 0
            minutes = int(minutes) if minutes else 0
            seconds = int(seconds) if seconds else 0
        except ValueError:
            # 如果输入无效，可以显示一个错误信息或者使用默认时间
            hours = 0
            minutes = 0
            seconds = 0

        total_seconds = hours * 3600 + minutes * 60 + seconds

        if sys.platform == 'win32':
            if total_seconds > 0:
                os.system(f'shutdown /s /t {total_seconds}')
            else:
                os.system('shutdown /s')
        elif sys.platform == 'linux' or sys.platform == 'darwin':
            if total_seconds > 0:
                os.system(f'sleep {total_seconds} && shutdown -h now')
            else:
                os.system('shutdown -h now')

    def cancel_action(self):
        if sys.platform == 'win32':
            os.system('shutdown /a')
        elif sys.platform == 'linux' or sys.platform == 'darwin':
            # 在Linux和macOS上取消挂起或关机操作比较复杂
            # 这里可以显示一条信息告知用户无法取消操作
            print("在Linux和macOS上无法取消挂起或关机操作")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShutdownTab()
    window.show()
    sys.exit(app.exec_())
