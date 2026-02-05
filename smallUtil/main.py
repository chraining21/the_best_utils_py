import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QDesktopWidget
from PyQt5.QtGui import QIcon 
from pathTrans import PathTransTab
from jsonFormatter import JsonFormatterTab
import qtawesome as qta
from md5Cal import MD5Cal
from stringTrans import StringTrans
from copyfile import CopyFileWindow
from copyfile_v2 import CopyFileWindow2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('SmallUtil')
        self.setGeometry(100, 100, 1800, 600)
        
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
        
        self.setWindowIcon(QIcon('./icon.ico'))

        # 創建Tab Widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 創建並添加各個分頁
        self.path_trans_tab = PathTransTab()
        json_icon = qta.icon('fa5s.truck-pickup') 
        self.tabs.addTab(self.path_trans_tab, json_icon, 'PathTrans')
        
        self.copy_file_tab = CopyFileWindow()
        json_icon = qta.icon('fa5s.yin-yang') 
        self.tabs.addTab(self.copy_file_tab, json_icon, 'Copy Files')
        
        self.copy_file_tab2 = CopyFileWindow2()
        json_icon = qta.icon('fa5s.yin-yang') 
        self.tabs.addTab(self.copy_file_tab2, json_icon, 'Copy Files2')

      
        # self.json_formatter_tab = JsonFormatterTab()
        # json_icon = qta.icon('fa5s.truck-moving')  # 使用 Font Awesome 的 code 图标
        # self.tabs.addTab(self.json_formatter_tab, json_icon, 'JsonFormat')

        self.md5 = MD5Cal()  # 创建 MD5Tab 实例
        json_icon = qta.icon('fa5s.truck-monster') 
        self.tabs.addTab(self.md5, json_icon, 'MD5')  # 添加 MD5Tab 分页
        
        # self.stringTrans = StringTrans()  # 创建 MD5Tab 实例
        # json_icon = qta.icon('fa5b.waze') 
        # self.tabs.addTab(self.stringTrans, json_icon, 'StringTrans')  # 添加 MD5Tab 分页
        
        # self.shutdown_tab = ShutdownTab()
        # self.tabs.addTab(self.shutdown_tab, '關機')

        # self.bash_command_tab = BatchCommandTab()
        # self.tabs.addTab(self.bash_command_tab, 'Batch 指令')
        
        # self.regex_tester_tab = RegexTesterTab()
        # self.tabs.addTab(self.regex_tester_tab, '正則測試')
        
        # self.text_comparer_tab = TextComparerTab()
        # self.tabs.addTab(self.text_comparer_tab, '文本對比')
        
        # self.md5_tab = MD5Tab()  # 创建 MD5Tab 实例
        # self.tabs.addTab(self.md5_tab, 'MD5 加密')  # 添加 MD5Tab 分页
        
        # self.code_snippet_manager_tab = CodeSnippetManagerTab()
        # self.tabs.addTab(self.code_snippet_manager_tab, '代码片段管理')

        # 這裡可以繼續添加其他分頁，例如：
        # self.xxx_tab = XxxTab()
        # self.tabs.addTab(self.xxx_tab, 'XXX')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow {
            font-family: 'Microsoft JhengHei';  
            font-size: 12pt;
            font-weight: bold;  /* 添加粗體 */
            background-color: #949188;
        }
        QTabWidget::tab {
            padding: 10px;
            font-size: 12pt;
            font-weight: bold;  /* 添加粗體 */
        }
        QTabBar::tab {
            background: #e0e0e0;  
            font-weight: bold;
            min-width: 120px;        /* 設定最小寬度 */
            padding: 10px 20px;      /* 上下10px、左右20px的內邊距 */
            margin-right: 2px;       /* tab之間的間距 */
        }
        QTabBar::tab:selected {
            background: #d0d0d0;  
        }
        QTabBar::tab:hover {
            background: #c0c0c0; 
        }
        QPushButton {
            background-color: #6b6657;  
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            font-size: 12pt;
            font-weight: bold;  /* 添加粗體 */
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #a8a085; 
        }
        QPushButton:pressed {
            background-color: #f5e9c1;  
        } 
        QLineEdit {
            padding: 5px;
            border: 1px solid #cccccc;
            border-radius: 3px;
            font-size: 12pt;
            font-weight: bold;  /* 添加粗體 */
        }
        QTextEdit {
            font-size: 12pt;
            font-weight: bold;  /* 添加粗體 */
        }
        QLabel {
            font-size: 12pt;
            font-weight: bold;  /* 添加粗體 */
        }
        QComboBox {
            font-size: 12pt;
            font-weight: bold;  /* 添加粗體 */
        }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# pyinstaller --name SmallUtil --windowed --icon=icon.ico --add-data "icon.ico;." --hidden-import PyQt5.sip main.py
