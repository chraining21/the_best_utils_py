import json
import re
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit,
    QPushButton, QLabel, QListWidget, QMessageBox, QFileDialog, QTabWidget, QInputDialog
)
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import Qt

class CodeHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # 关键字
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor('blue'))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            'class', 'def', 'return', 'if', 'else', 'elif', 'while', 'for', 'try', 'except',
            'with', 'as', 'import', 'from', 'pass', 'break', 'continue', 'in', 'and', 'or', 'not'
        ]
        self.highlighting_rules = [(re.compile(r'\b' + kw + r'\b'), keyword_format) for kw in keywords]

        # 注释
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor('green'))
        self.highlighting_rules.append((re.compile(r'#.*'), comment_format))

        # 字符串
        string_format = QTextCharFormat()
        string_format.setForeground(QColor('magenta'))
        self.highlighting_rules.append((re.compile(r'".*?"'), string_format))
        self.highlighting_rules.append((re.compile(r"'.*?'"), string_format))

    def highlightBlock(self, text):
        for pattern, char_format in self.highlighting_rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, char_format)

class CodeSnippetManagerTab(QWidget):
    def __init__(self):
        super().__init__()

        self.snippets = {}
        self.category_tabs = {}
        self.current_snippet = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 搜索框区域
        self.search_layout = QHBoxLayout()

        self.search_label = QLabel('搜索:')
        self.search_layout.addWidget(self.search_label)

        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_snippets)
        self.search_layout.addWidget(self.search_input)

        self.layout.addLayout(self.search_layout)

        # 添加代码片段区域
        self.add_snippet_layout = QHBoxLayout()

        self.title_label = QLabel('标题:')
        self.add_snippet_layout.addWidget(self.title_label)

        self.title_input = QLineEdit()
        self.add_snippet_layout.addWidget(self.title_input)

        self.category_label = QLabel('类别:')
        self.add_snippet_layout.addWidget(self.category_label)

        self.category_input = QLineEdit()
        self.add_snippet_layout.addWidget(self.category_input)

        self.layout.addLayout(self.add_snippet_layout)

        self.code_input = QTextEdit()
        self.layout.addWidget(self.code_input)

        # 添加代码高亮功能
        self.highlighter = CodeHighlighter(self.code_input.document())

        self.add_button = QPushButton('添加代码片段')
        self.add_button.clicked.connect(self.add_snippet)
        self.layout.addWidget(self.add_button)

        # 标签页区域
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # 保存和加载代码片段
        self.save_button = QPushButton('保存代码片段到文件')
        self.save_button.clicked.connect(self.save_snippets)
        self.layout.addWidget(self.save_button)

        self.load_button = QPushButton('从文件加载代码片段')
        self.load_button.clicked.connect(self.load_snippets)
        self.layout.addWidget(self.load_button)

    def add_snippet(self):
        title = self.title_input.text()
        category = self.category_input.text()
        code = self.code_input.toPlainText()

        if not title or not category or not code:
            QMessageBox.warning(self, '警告', '所有字段都是必需的')
            return

        if category not in self.snippets:
            self.snippets[category] = {}
            self.add_category_tab(category)

        self.snippets[category][title] = code
        self.update_category_tab(category)

        self.title_input.clear()
        self.category_input.clear()
        self.code_input.clear()

    def add_category_tab(self, category):
        tab = QWidget()
        tab.layout = QVBoxLayout()
        tab.setLayout(tab.layout)

        snippet_list = QListWidget()
        snippet_list.itemClicked.connect(self.load_snippet)
        tab.layout.addWidget(snippet_list)

        edit_button = QPushButton('编辑代码片段')
        edit_button.clicked.connect(lambda: self.edit_snippet(category))
        tab.layout.addWidget(edit_button)

        delete_button = QPushButton('删除代码片段')
        delete_button.clicked.connect(lambda: self.delete_snippet(category))
        tab.layout.addWidget(delete_button)

        rename_button = QPushButton('重命名类别')
        rename_button.clicked.connect(lambda: self.rename_category(category))
        tab.layout.addWidget(rename_button)

        self.tab_widget.addTab(tab, category)
        self.category_tabs[category] = tab

    def update_category_tab(self, category):
        tab = self.category_tabs[category]
        snippet_list = tab.layout.itemAt(0).widget()
        snippet_list.clear()
        for title in self.snippets[category].keys():
            snippet_list.addItem(title)

    def remove_category_tab(self, category):
        index = self.tab_widget.indexOf(self.category_tabs[category])
        self.tab_widget.removeTab(index)
        del self.category_tabs[category]

    def load_snippet(self, item):
        category = self.tab_widget.tabText(self.tab_widget.currentIndex())
        title = item.text()
        snippet = self.snippets[category][title]

        self.title_input.setText(title)
        self.category_input.setText(category)
        self.code_input.setText(snippet)

        self.current_snippet = (category, title)

    def edit_snippet(self, category):
        if not self.current_snippet:
            QMessageBox.warning(self, '警告', '请选择一个代码片段进行编辑')
            return

        old_category, old_title = self.current_snippet

        title = self.title_input.text()
        new_category = self.category_input.text()
        code = self.code_input.toPlainText()

        if not title or not new_category or not code:
            QMessageBox.warning(self, '警告', '所有字段都是必需的')
            return

        if old_category != new_category:
            del self.snippets[old_category][old_title]
            if not self.snippets[old_category]:
                del self.snippets[old_category]
                self.remove_category_tab(old_category)
            
            if new_category not in self.snippets:
                self.snippets[new_category] = {}
                self.add_category_tab(new_category)

        self.snippets[new_category][title] = code
        self.update_category_tab(new_category)

        self.title_input.clear()
        self.category_input.clear()
        self.code_input.clear()
        self.current_snippet = None

    def delete_snippet(self, category):
        if not self.current_snippet:
            QMessageBox.warning(self, '警告', '请选择一个代码片段进行删除')
            return

        old_category, old_title = self.current_snippet

        del self.snippets[old_category][old_title]
        if not self.snippets[old_category]:
            del self.snippets[old_category]
            self.remove_category_tab(old_category)
        else:
            self.update_category_tab(old_category)

        self.title_input.clear()
        self.category_input.clear()
        self.code_input.clear()
        self.current_snippet = None

    def rename_category(self, category):
        new_category, ok = QInputDialog.getText(self, '重命名类别', '请输入新的类别名称:')
        if ok and new_category:
            if new_category in self.snippets:
                QMessageBox.warning(self, '警告', '类别名称已存在')
                return

            # 更新 self.snippets 和 self.category_tabs
            self.snippets[new_category] = self.snippets.pop(category)
            self.category_tabs[new_category] = self.category_tabs.pop(category)

            # 更新标签页上的类别名称
            index = self.tab_widget.indexOf(self.category_tabs[new_category])
            self.tab_widget.setTabText(index, new_category)

            # 更新按钮绑定的新类别
            tab = self.category_tabs[new_category]
            tab.layout.itemAt(1).widget().clicked.disconnect()
            tab.layout.itemAt(1).widget().clicked.connect(lambda: self.edit_snippet(new_category))
            tab.layout.itemAt(2).widget().clicked.disconnect()
            tab.layout.itemAt(2).widget().clicked.connect(lambda: self.delete_snippet(new_category))
            tab.layout.itemAt(3).widget().clicked.disconnect()
            tab.layout.itemAt(3).widget().clicked.connect(lambda: self.rename_category(new_category))

            # 更新标签页内容
            self.update_category_tab(new_category)

    def save_snippets(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, '保存代码片段', '', 'JSON Files (*.json);;All Files (*)', options=options)
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.snippets, file, ensure_ascii=False, indent=4)
            QMessageBox.information(self, '信息', '代码片段已成功保存')

    def load_snippets(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, '打开代码片段文件', '', 'JSON Files (*.json);;All Files (*)', options=options)
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.snippets = json.load(file)
            self.tab_widget.clear()
            self.category_tabs.clear()
            for category in self.snippets:
                self.add_category_tab(category)
                self.update_category_tab(category)
            QMessageBox.information(self, '信息', '代码片段已成功加载')

    def search_snippets(self):
        query = self.search_input.text().lower()
        for category, snippets in self.snippets.items():
            for title, code in snippets.items():
                if query in title.lower() or query in code.lower():
                    # 显示匹配的代码片段
                    self.tab_widget.setCurrentWidget(self.category_tabs[category])
                    snippet_list = self.category_tabs[category].layout.itemAt(0).widget()
                    items = snippet_list.findItems(title, Qt.MatchExactly)
                    if items:
                        snippet_list.setCurrentItem(items[0])
                        self.load_snippet(items[0])
                        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CodeSnippetManagerTab()
    window.show()
    sys.exit(app.exec_())
