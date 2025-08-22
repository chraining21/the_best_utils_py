# 文件: xxx.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class XxxTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel('這是XXX分頁')
        self.layout.addWidget(self.label)

# 在main.py中

from xxx import XxxTab

# 添加以下兩行代碼到 __init__ 方法中
self.xxx_tab = XxxTab()



"""
运行程序：
确保所有文件都在同一个目录下，然后运行 main.py。

打包程序：
创建一个 pyinstaller 的打包配置文件，确保所有分页面模块都能被正确打包。使用 pyinstaller 打包时，执行以下命令：

pyinstaller --onefile --windowed main.py

"""