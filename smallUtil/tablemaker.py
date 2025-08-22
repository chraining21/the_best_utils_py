import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

class TableMaker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dynamic Table Generator')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.input_edit = QTextEdit()
        input_layout.addWidget(self.input_edit)

        layout.addLayout(input_layout)

        self.generate_btn = QPushButton("生成表格")
        self.generate_btn.clicked.connect(self.generate_table)
        layout.addWidget(self.generate_btn)

        self.table = QTableWidget(self)
        self.table.setSelectionBehavior(QTableWidget.SelectItems)  # 选择单元格
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)  # 扩展选择模式
        layout.addWidget(self.table)

        self.setLayout(layout)

    def generate_table(self):
        data_string = self.input_edit.toPlainText()
        data = [line.split() for line in data_string.strip().split('\n')]

        rows = len(data)
        cols = len(data[0]) if rows > 0 else 0

        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)

        for i in range(rows):
            for j in range(cols):
                self.table.setItem(i, j, QTableWidgetItem(data[i][j]))

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self.copy_selection()

    def copy_selection(self):
        selected_ranges = self.table.selectedRanges()
        if not selected_ranges:
            return

        selected_text = ''
        for selection_range in selected_ranges:
            for i in range(selection_range.topRow(), selection_range.bottomRow() + 1):
                row_text = []
                for j in range(selection_range.leftColumn(), selection_range.rightColumn() + 1):
                    item = self.table.item(i, j)
                    if item:
                        row_text.append(item.text())
                    else:
                        row_text.append('')
                selected_text += '\t'.join(row_text) + '\n'

        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TableMaker()
    ex.show()
    sys.exit(app.exec_())
