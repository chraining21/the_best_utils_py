from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
                           QTextEdit, QLabel, QApplication, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
import os
import shutil
import glob
import re
import json
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

class CopyFileWindow2(QWidget):
    def __init__(self):
        super().__init__()
        self.config_file = "copyfile_config2.json"
        self.paths_data = self.load_config()
        
        # 創建主布局
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # 起始路徑選擇和管理
        start_path_layout = QHBoxLayout()
        self.start_path_label = QLabel("檔案起始路徑:")
        self.start_path_select = QComboBox()
        self.start_path_select.setEditable(True)
        self.start_path_select.addItems(self.paths_data.get("start_paths", []))
        self.start_path_select.setMinimumWidth(200)  # 設置最小寬度
        self.start_path_add = QPushButton("Add")
        self.start_path_delete = QPushButton("Del")
        self.start_path_add.setFixedWidth(80)
        self.start_path_delete.setFixedWidth(80)
        
        start_path_layout.addWidget(self.start_path_label)
        start_path_layout.addWidget(self.start_path_select, 1)
        start_path_layout.addWidget(self.start_path_add)
        start_path_layout.addWidget(self.start_path_delete)
        self.layout.addLayout(start_path_layout)
        
        # 修改輸出路徑部分，添加檔案列表顯示
        output_section = QVBoxLayout()
        
        # 輸出路徑選擇和管理
        output_path_layout = QHBoxLayout()
        self.output_path_label = QLabel("結果輸出路徑:")
        self.output_path_select = QComboBox()
        self.output_path_select.setEditable(True)
        self.output_path_select.setMinimumWidth(200)
        self.output_path_add = QPushButton("Add")
        self.output_path_delete = QPushButton("Del")
        self.output_path_save = QPushButton("Save Files")  # 新增儲存按鈕
        
        output_path_layout.addWidget(self.output_path_label)
        output_path_layout.addWidget(self.output_path_select, 1)
        output_path_layout.addWidget(self.output_path_add)
        output_path_layout.addWidget(self.output_path_delete)
        output_path_layout.addWidget(self.output_path_save)
        
        output_section.addLayout(output_path_layout)
        
        self.layout.addLayout(output_section)
     
        
        # 檔案路徑輸入區域
        self.files_label = QLabel("需要被複製的檔案路徑 (每行一個):")
        self.layout.addWidget(self.files_label)
        
        self.files_input = QTextEdit()
        self.files_input.setPlaceholderText("在此輸入檔案路徑，每行一個...")
        self.layout.addWidget(self.files_input)
        
        # 複製按鈕
        self.copy_button = QPushButton("確認複製")
        self.copy_button.clicked.connect(self.copy_files)
        self.layout.addWidget(self.copy_button)

        # 連接按鈕事件
        self.start_path_add.clicked.connect(lambda: self.add_path("start_paths"))
        self.start_path_delete.clicked.connect(lambda: self.delete_path("start_paths"))
        self.output_path_add.clicked.connect(lambda: self.add_path("output_paths"))
        self.output_path_delete.clicked.connect(lambda: self.delete_path("output_paths"))
        self.output_path_select.currentIndexChanged.connect(self.on_output_path_changed)
        self.output_path_save.clicked.connect(self.save_current_files)
        # 添加快捷鍵
        # 儲存檔案清單的快捷鍵
        self.save_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        self.save_shortcut.activated.connect(self.save_current_files)

        # 儲存起始路徑的快捷鍵
        self.save_start_path_shortcut = QShortcut(QKeySequence('Ctrl+D'), self)
        self.save_start_path_shortcut.activated.connect(lambda: self.add_path("start_paths"))

        # 儲存輸出路徑的快捷鍵
        self.save_output_path_shortcut = QShortcut(QKeySequence('Ctrl+Shift+D'), self)
        self.save_output_path_shortcut.activated.connect(lambda: self.add_path("output_paths"))

        # 在按鈕上添加提示文字
        self.start_path_add.setToolTip("快捷鍵: Ctrl+D")
        self.output_path_add.setToolTip("快捷鍵: Ctrl+Shift+D")
        self.output_path_save.setToolTip("快捷鍵: Ctrl+S")
        
        # 更新輸出路徑下拉選單
        self.update_output_paths()

    def load_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {
                    "start_paths": data.get("start_paths", []),
                    "output_configs": data.get("output_configs", [])
                }
        except (FileNotFoundError, json.JSONDecodeError):
            return {"start_paths": [], "output_configs": []}

    def update_output_paths(self):
        self.output_path_select.clear()
        for config in self.paths_data["output_configs"]:
            self.output_path_select.addItem(config["output_path"])
            
        if self.paths_data["output_configs"]:
            # 載入第一個輸出路徑的檔案清單
            first_config = self.paths_data["output_configs"][0]
            self.files_input.setText("\n".join(first_config["files"]))

    def on_output_path_changed(self, index):
        if index >= 0:
            current_path = self.output_path_select.currentText()
            # 找到對應的設定
            for config in self.paths_data["output_configs"]:
                if config["output_path"] == current_path:
                    self.files_input.setText("\n".join(config["files"]))
                    break

    def save_current_files(self):
        current_path = self.output_path_select.currentText()
        current_files = self.files_input.toPlainText().strip().splitlines()
        
        # 更新或新增設定
        found = False
        for config in self.paths_data["output_configs"]:
            if config["output_path"] == current_path:
                config["files"] = current_files
                found = True
                break
                
        if not found:
            self.paths_data["output_configs"].append({
                "output_path": current_path,
                "files": current_files
            })
            
        self.save_config()
        QMessageBox.information(self, "成功", "檔案清單已儲存")

    def add_path(self, path_type):
        if path_type == "start_paths":
            current_path = self.start_path_select.currentText().strip()
            if not current_path:
                return
                
            if current_path not in self.paths_data[path_type]:
                self.paths_data[path_type].append(current_path)
                if self.start_path_select.findText(current_path) == -1:
                    self.start_path_select.addItem(current_path)
                self.save_config()
                QMessageBox.information(self, "成功", "路徑已新增")
            else:
                QMessageBox.warning(self, "警告", "此路徑已存在")
        else:
            current_path = self.output_path_select.currentText().strip()
            if not current_path:
                return
                
            # 檢查是否已存在
            exists = False
            for config in self.paths_data["output_configs"]:
                if config["output_path"] == current_path:
                    exists = True
                    break
                    
            if not exists:
                self.paths_data["output_configs"].append({
                    "output_path": current_path,
                    "files": []
                })
                self.update_output_paths()
                self.save_config()
                QMessageBox.information(self, "成功", "輸出路徑已新增")
            else:
                QMessageBox.warning(self, "警告", "此路徑已存在")

    def delete_path(self, path_type):
        if path_type == "start_paths":
            current_path = self.start_path_select.currentText()
            if current_path in self.paths_data[path_type]:
                self.paths_data[path_type].remove(current_path)
                self.start_path_select.removeItem(self.start_path_select.currentIndex())
                self.save_config()
                QMessageBox.information(self, "成功", "路徑已刪除")
            else:
                QMessageBox.warning(self, "警告", "找不到要刪除的路徑")
        else:
            current_path = self.output_path_select.currentText()
            
            # 移除對應的設定
            self.paths_data["output_configs"] = [
                config for config in self.paths_data["output_configs"]
                if config["output_path"] != current_path
            ]
            
            self.update_output_paths()
            self.save_config()
            QMessageBox.information(self, "成功", "輸出路徑已刪除")
            
    def copy_files(self):
        start_path = self.start_path_select.currentText().strip()
        output_path = self.output_path_select.currentText().strip()
        file_paths = self.files_input.toPlainText().strip().splitlines()

        if not start_path or not output_path:
            QMessageBox.warning(self, "警告", "請選擇起始路徑和輸出路徑")
            return

        success_count = 0
        error_messages = []
        
        # 支援的檔案類型
        web_extensions = [".html", ".js", ".jsp", ".css"]
        
        # 檢查輸入路徑，分類為兩種類型
        filename_only_paths = []
        web_paths = []
        
        for file_path in file_paths:
            file_path = file_path.strip()
            if not file_path:
                continue
            
            # 檢查是否是前端檔案路徑 (包含斜線或反斜線)
            if '/' in file_path or '\\' in file_path:
                web_paths.append(file_path)
            else:
                # 檢查是否只有檔案名稱
                filename_only_paths.append(file_path)
        
        # 處理只有檔案名稱的路徑
        for filename in filename_only_paths:
            found_any = False
            
            # 遞迴搜尋檔案
            for root, _, files in os.walk(start_path):
                for file in files:
                    # 檢查檔案名稱是否匹配
                    if file == filename or file.lower() == filename.lower():
                        # 檢查副檔名是否為支援的類型
                        _, ext = os.path.splitext(file)
                        if ext.lower() in web_extensions:
                            found_any = True
                            source_file = os.path.join(root, file)
                            # 計算相對路徑
                            rel_path = os.path.relpath(source_file, start_path)
                            destination_file = os.path.join(output_path, rel_path)

                            try:
                                os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                                shutil.copy(source_file, destination_file)
                                success_count += 1
                            except Exception as e:
                                error_messages.append(f"複製檔案時發生錯誤: {source_file}\n錯誤訊息: {str(e)}")
            
            if not found_any:
                error_messages.append(f"找不到任何符合的檔案: {filename}")
        
        # 處理前端檔案路徑
        for file_path in web_paths:
            found_any = False
            # 將路徑中的正斜線轉換為系統適用的分隔符
            file_path = file_path.replace('/', os.sep).replace('\\', os.sep)
            
            # 直接尋找檔案
            source_file = os.path.join(start_path, file_path)
            
            if os.path.exists(source_file):
                # 檢查副檔名是否為支援的類型
                _, ext = os.path.splitext(source_file)
                if ext.lower() in web_extensions:
                    found_any = True
                    # 計算相對路徑
                    rel_path = os.path.relpath(source_file, start_path)
                    destination_file = os.path.join(output_path, rel_path)

                    try:
                        os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                        shutil.copy(source_file, destination_file)
                        success_count += 1
                    except Exception as e:
                        error_messages.append(f"複製檔案時發生錯誤: {source_file}\n錯誤訊息: {str(e)}")
            
            if not found_any:
                error_messages.append(f"找不到任何符合的檔案: {file_path}")

        if success_count > 0:
            QMessageBox.information(self, "成功", f"成功複製了 {success_count} 個檔案。")
        if error_messages:
            QMessageBox.warning(self, "警告", "\n".join(error_messages))


            
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.paths_data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = CopyFileWindow2()
    window.show()
    sys.exit(app.exec_())
