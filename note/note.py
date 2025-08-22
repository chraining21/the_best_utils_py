import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import re
import os

class WorkLogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("工作紀錄")
        
        # 設定視窗大小
        self.root.geometry("700x500")
        
        icon_path_png = "icon.png"
        if os.path.exists(icon_path_png):
            icon = tk.PhotoImage(file=icon_path_png)
            self.root.iconphoto(True, icon)
        
        # 創建 Notebook（分頁）
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill="both")
        
       
        # 創建兩個分頁
        self.input_frame = ttk.Frame(self.notebook)
        self.log_frame = ttk.Frame(self.notebook)
        self.today_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.input_frame, text="輸入紀錄")
        self.notebook.add(self.log_frame, text="顯示紀錄")
        self.notebook.add(self.today_frame, text="今天的紀錄")

        # 定義字體
        self.label_font = ("微軟正黑體", 12, "bold")
        self.input_font = ("微軟正黑體", 11)
        self.log_font = ("微軟正黑體", 10)
        
        # 輸入分頁的內容
        self.input_label = ttk.Label(self.input_frame, text="請輸入工作內容：", font=self.label_font, foreground="#2c3e50")
        self.input_label.pack(pady=10)
        
        self.input_text = tk.Text(self.input_frame, height=10, width=70, font=self.input_font, foreground="#34495e", background="#ecf0f1", borderwidth=2, relief="groove")
        self.input_text.pack(pady=5, padx=10)
        
        # 提示用戶使用 Ctrl+S 儲存
        self.save_label = ttk.Label(self.input_frame, text="按 Ctrl+S 儲存紀錄", font=("微軟正黑體", 10), foreground="#7f8c8d")
        self.save_label.pack(pady=5)
        
        # 顯示紀錄分頁的內容
        self.log_text = tk.Text(self.log_frame, height=20, width=70, font=self.log_font, foreground="#2c3e50", background="#f8f9fa", borderwidth=2, relief="groove")
        self.log_text.pack(pady=10, padx=10, fill="both", expand=True)
        
         # 今天的紀錄分頁內容
        self.today_text = tk.Text(self.today_frame, height=20, width=70, font=self.log_font, 
                                foreground="#2c3e50", background="#f8f9fa", 
                                borderwidth=2, relief="groove")
        self.today_text.pack(pady=10, padx=10, fill="both", expand=True)
        
        # 綁定 Ctrl+S 事件
        self.root.bind('<Control-s>', self.save_log)
        
        # 初始化時載入歷史紀錄
        self.load_logs()
        self.load_today_logs()

    
    def get_weekday_chinese(self, date):
        # 將星期幾轉換為中文
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        return weekdays[date.weekday()]
    
    def save_log(self, event=None):
        # 獲取當前時間
        current_time = datetime.now()
        timestamp = f"[{current_time.strftime('%Y-%m-%d')} {current_time.strftime('%H:%M:%S')}]"
        
        # 獲取輸入的內容
        content = self.input_text.get("1.0", tk.END).strip()
        
        if content:
            # 處理多行文字
            lines = content.split('\n')
            log_entries = []
            
            # 第一行
            first_line = f"{timestamp} {lines[0]}\n"
            log_entries.append(first_line)
            
            # 計算縮排空格數（時間戳記長度加一個空格）
            indent = " " * 63
            
            # 處理後續行
            for line in lines[1:]:
                if line.strip():  # 只處理非空行
                    log_entry = f"{indent}{line}\n"
                    log_entries.append(log_entry)
            
            # 最後加入一個空行
            log_entries.append("\n")
            
            # 寫入檔案
            with open("work_log.txt", "a", encoding="utf-8") as f:
                f.writelines(log_entries)
            
            # 清空輸入框
            self.input_text.delete("1.0", tk.END)
            # 更新紀錄顯示
            self.load_logs()
            self.load_today_logs()


    def load_logs(self):
        # 清空目前的顯示內容
        self.log_text.delete("1.0", tk.END)
        try:
            # 讀取檔案
            with open("work_log.txt", "r", encoding="utf-8") as f:
                logs = f.readlines()
            
            if not logs:
                self.log_text.insert(tk.END, "尚未有任何紀錄。\n")
                return
            
            # 用來儲存按週分類的紀錄
            weekly_logs = {}
            current_entry = []
            current_date = None
            
            for log in logs:
                # 修改正則表達式以匹配兩種格式
                match = re.match(r'\[(\d{4}-\d{2}-\d{2})(?:\s+星期[一二三四五六日])?\s+(\d{2}:\d{2}:\d{2})\]', log)
                if match:
                    # 如果有之前的條目，先儲存它
                    if current_entry:
                        if current_date and week_key in weekly_logs:
                            weekly_logs[week_key][current_date].append(''.join(current_entry))
                    
                    # 開始新的條目
                    date_str = match.group(1)
                    time_str = match.group(2)
                    current_date = date_str
                    log_date = datetime.strptime(date_str, "%Y-%m-%d")
                    
                    # 轉換格式：添加星期
                    weekday = self.get_weekday_chinese(log_date)
                    new_timestamp = f"[{date_str} {weekday} {time_str}]"
                    
                    # 保留原始內容的其餘部分
                    original_content = log[log.find(']')+1:].rstrip()
                    current_entry = [f"{new_timestamp}{original_content}\n"]
                    
                    # 獲取該日期所在週的週一
                    monday = log_date - timedelta(days=log_date.weekday())
                    week_key = monday.strftime("%Y-%m-%d")
                    
                    # 初始化週和日的字典
                    if week_key not in weekly_logs:
                        weekly_logs[week_key] = {}
                    if current_date not in weekly_logs[week_key]:
                        weekly_logs[week_key][current_date] = []
                else:
                    if current_entry:
                        # 保持原有的縮排格式
                        current_entry.append(log)
            
            # 處理最後一個條目
            if current_entry:
                if current_date and week_key in weekly_logs:
                    weekly_logs[week_key][current_date].append(''.join(current_entry))
            
            # 顯示邏輯保持不變
            sorted_weeks = sorted(weekly_logs.keys(), reverse=True)
            for week_start in sorted_weeks:
                week_start_date = datetime.strptime(week_start, "%Y-%m-%d")
                week_end_date = week_start_date + timedelta(days=6)
                
                week_number = week_start_date.isocalendar()[1]
                start_weekday = self.get_weekday_chinese(week_start_date)
                end_weekday = self.get_weekday_chinese(week_end_date)
                
                week_label = f"第 {week_number} 週 ({week_start_date.strftime('%Y-%m-%d')} {start_weekday} ~ {week_end_date.strftime('%Y-%m-%d')} {end_weekday})\n"
                self.log_text.insert(tk.END, "=" * 50 + "\n")
                self.log_text.insert(tk.END, week_label)
                self.log_text.insert(tk.END, "=" * 50 + "\n")
                
                sorted_days = sorted(weekly_logs[week_start].keys(), reverse=True)
                for day in sorted_days:
                    daily_logs = weekly_logs[week_start][day]
                    daily_logs.sort(key=lambda x: re.search(r'\d{2}:\d{2}:\d{2}', x).group() if re.search(r'\d{2}:\d{2}:\d{2}', x) else '', reverse=True)
                    
                    for log in daily_logs:
                        self.log_text.insert(tk.END, log)
                    
                    if day != sorted_days[-1]:
                        self.log_text.insert(tk.END, "-" * 50 + "\n")
                
                self.log_text.insert(tk.END, "\n")
                
        except FileNotFoundError:
            self.log_text.insert(tk.END, "尚未有任何紀錄。\n")

    def load_today_logs(self):
        self.today_text.delete("1.0", tk.END)
        try:
            with open("work_log.txt", "r", encoding="utf-8") as f:
                logs = f.readlines()
            
            if not logs:
                self.today_text.insert(tk.END, "今天尚未有任何紀錄。\n")
                return
            
            # 獲取今天的日期
            today = datetime.now().strftime("%Y-%m-%d")
            current_entry = []
            today_logs = []
            
            for log in logs:
                match = re.match(r'\[(\d{4}-\d{2}-\d{2})(?:\s+星期[一二三四五六日])?\s+(\d{2}:\d{2}:\d{2})\]', log)
                if match:
                    # 如果有之前的條目，先儲存它
                    if current_entry:
                        today_logs.append(current_entry)
                        current_entry = []
                    
                    date_str = match.group(1)
                    time_str = match.group(2)
                    
                    # 只處理今天的紀錄
                    if date_str == today:
                        log_date = datetime.strptime(date_str, "%Y-%m-%d")
                        weekday = self.get_weekday_chinese(log_date)
                        new_timestamp = f"[{date_str} {weekday} {time_str}]"
                        original_content = log[log.find(']')+1:].rstrip()
                        current_entry = [f"{new_timestamp}{original_content}\n", time_str]
                else:
                    if current_entry:
                        current_entry.insert(-1, log)
            
            # 處理最後一個條目（移到迴圈外）
            if current_entry:
                today_logs.append(current_entry)
            
            # 根據時間戳排序（由舊到新）
            today_logs.sort(key=lambda x: x[-1])
            
            if today_logs:
                self.today_text.insert(tk.END, f"=== {today} 的工作紀錄 ===\n")
                for log_entry in today_logs:
                    content = ''.join(log_entry[:-1])
                    self.today_text.insert(tk.END, content)
            else:
                self.today_text.insert(tk.END, "今天尚未有任何紀錄。\n")
                    
        except FileNotFoundError:
            self.today_text.insert(tk.END, "尚未有任何紀錄。\n")




if __name__ == "__main__":
    root = tk.Tk()
    app = WorkLogApp(root)
    root.mainloop()

##pyinstaller --onefile --windowed note.py