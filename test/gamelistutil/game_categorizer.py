import tkinter as tk
from tkinter import messagebox, ttk
import json
from collections import defaultdict

class GameCategorizerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.tabs = {}
    
    def init_ui(self):
        # 創建上下分割的面板
        self.paned_window = ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 創建輸入區域
        self.input_frame = ttk.LabelFrame(self.paned_window, text="JSON 資料輸入")
        self.paned_window.add(self.input_frame, weight=1)
        
        # 創建輸入文本框和滾動條
        self.input_text_frame = ttk.Frame(self.input_frame)
        self.input_text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.input_scrollbar = ttk.Scrollbar(self.input_text_frame)
        self.input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.input_text = tk.Text(self.input_text_frame, yscrollcommand=self.input_scrollbar.set)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        self.input_scrollbar.config(command=self.input_text.yview)
        
        # 創建按鈕框架
        self.button_frame = ttk.Frame(self.input_frame)
        self.button_frame.pack(fill=tk.X, pady=5)
        
        # 創建解析按鈕
        self.parse_button = ttk.Button(self.button_frame, text="解析並分類", command=self.parse_json)
        self.parse_button.pack(side=tk.LEFT, padx=5)
        
        # 創建清除按鈕
        self.clear_button = ttk.Button(self.button_frame, text="清除輸入", command=self.clear_input)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # 創建結果區域
        self.result_frame = ttk.LabelFrame(self.paned_window, text="分類結果")
        self.paned_window.add(self.result_frame, weight=2)
        
        # 創建選項卡
        self.notebook = ttk.Notebook(self.result_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def parse_json(self):
        """解析輸入的JSON資料"""
        json_text = self.input_text.get("1.0", tk.END).strip()
        if not json_text:
            messagebox.showwarning("警告", "請輸入JSON資料")
            return
        
        try:
            games_data = json.loads(json_text)
            games_data = games_data['result']
            self.categorized_games = self.categorize_games(games_data)
            self.create_category_tabs()
            messagebox.showinfo("成功", "JSON資料解析成功並已分類")
        except json.JSONDecodeError as e:
            messagebox.showerror("錯誤", f"JSON格式錯誤: {str(e)}")
    
    def clear_input(self):
        """清除輸入框內容"""
        self.input_text.delete("1.0", tk.END)
    
    def categorize_games(self, games):
        """按類別分組遊戲"""
        categorized = defaultdict(list)
        for game in games:
            categorized[game['category']].append(game)
        return categorized
    
    def create_category_tabs(self):
        """創建類別標籤頁"""
        # 清除現有標籤頁
        for tab_id in self.notebook.tabs():
            self.notebook.forget(tab_id)
        
        self.tabs = {}
        
        # 為每個類別創建新標籤頁
        for category in sorted(self.categorized_games.keys()):
            self.create_category_tab(category)
    
    def create_category_tab(self, category):
        """為每個類別創建標籤頁"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=f"{category} ({len(self.categorized_games[category])})")
        
        # 創建頂部按鈕框架 - 確保複製按鈕在頂部顯示
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill=tk.X, pady=5)
        
        # 創建複製按鈕 - 放在頂部
        copy_button = ttk.Button(
            button_frame, 
            text=f"複製 {category} 類別資料", 
            command=lambda cat=category: self.copy_category_data(cat)
        )
        copy_button.pack(side=tk.LEFT, padx=5)
        
        # 創建文本區域和滾動條
        text_frame = ttk.Frame(tab)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_area = tk.Text(text_frame, yscrollcommand=scrollbar.set)
        text_area.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_area.yview)
        
        # 將遊戲數據格式化並插入文本區域
        formatted_data = json.dumps(self.categorized_games[category], ensure_ascii=False, indent=4)
        text_area.insert(tk.END, formatted_data)
        text_area.config(state=tk.DISABLED)  # 設為只讀
        
        self.tabs[category] = {
            'tab': tab,
            'text_area': text_area,
            'data': formatted_data
        }
    
    def copy_category_data(self, category):
        """複製特定類別的數據到剪貼板"""
        data = self.tabs[category]['data']
        self.clipboard_clear()
        self.clipboard_append(data)
        self.update()  # 更新剪貼簿
        
        # 顯示複製成功的提示
        messagebox.showinfo("提示", f"{category} 類別資料已複製到剪貼簿!")
