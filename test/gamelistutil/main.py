import tkinter as tk
import tkinter.ttk as ttk 
import os
import sys
from data_processor import DataProcessorFrame
from game_categorizer import GameCategorizerFrame
from gamelist_dealer import GameProcessorFrame

class GameToolsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("遊戲資料處理工具")
        self.root.geometry("500x700")
        
        # 設置視窗最小尺寸
        self.root.minsize(500, 700)
        
        # 創建主框架
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 創建主選項卡
        self.main_notebook = ttk.Notebook(self.main_frame)
        self.main_notebook.pack(fill=tk.BOTH, expand=True)
       
        # 創建第1個分頁 - 遊戲分類工具
        self.game_categorizer = GameCategorizerFrame(self.main_notebook)
        self.main_notebook.add(self.game_categorizer, text="遊戲分類工具")
        
        # 創建第2個分頁 - 資料處理工具
        self.data_processor = DataProcessorFrame(self.main_notebook)
        self.main_notebook.add(self.data_processor, text="資料處理工具")
        
        # 創建第3個分頁 - gamelist
        self.processor_frame = GameProcessorFrame(self.main_notebook)
        self.main_notebook.add(self.processor_frame, text="遊戲列表處理器")
        
        # 設置狀態欄
        self.status_bar = tk.Label(root, text="就緒", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
def main():
    """主函數，啟動應用程式"""
    root = tk.Tk()
    
    # 設置主題樣式
    style = ttk.Style()
    available_themes = style.theme_names()
    if 'vista' in available_themes:
        style.theme_use('vista')
    elif 'clam' in available_themes:
        style.theme_use('clam')
    
    app = GameToolsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
