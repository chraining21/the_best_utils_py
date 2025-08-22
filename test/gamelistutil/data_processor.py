import tkinter as tk
from tkinter import messagebox, ttk
import json

class DataProcessorFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # 初始化UI元素
        self.init_ui()
        
    def init_ui(self):
        # 創建Canvas和捲軸
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # 放置Canvas和捲軸
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 創建主框架放在Canvas上
        self.main_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # 綁定事件
        self.main_frame.bind("<Configure>", lambda e: self.on_frame_configure())
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # 輸入區域
        input_frame = ttk.LabelFrame(self.main_frame, text="輸入區域")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 輸入框標籤
        input_label = ttk.Label(input_frame, text="請輸入 JSON 資料：")
        input_label.pack(padx=5, pady=2)
        
        # 輸入框和捲軸
        input_scroll = ttk.Scrollbar(input_frame)
        input_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_textbox = tk.Text(input_frame, height=10, width=60, yscrollcommand=input_scroll.set)
        self.input_textbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        input_scroll.config(command=self.input_textbox.yview)
        
        # 處理按鈕
        process_button = ttk.Button(input_frame, text="處理資料", command=self.process_data)
        process_button.pack(pady=5)
        
        # 輸出區域
        output_frame = ttk.LabelFrame(self.main_frame, text="輸出區域")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 第一組輸出
        group1_frame = ttk.Frame(output_frame)
        group1_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        output_label1 = ttk.Label(group1_frame, text="第一組輸出結果：")
        output_label1.pack(anchor=tk.W)
        
        output_scroll1 = ttk.Scrollbar(group1_frame)
        output_scroll1.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_textbox1 = tk.Text(group1_frame, height=4, width=60, yscrollcommand=output_scroll1.set)
        self.output_textbox1.pack(fill=tk.BOTH, expand=True)
        output_scroll1.config(command=self.output_textbox1.yview)
        
        copy_button1 = ttk.Button(group1_frame, text="複製第一組資料", 
                                 command=lambda: self.copy_to_clipboard(self.output_textbox1))
        copy_button1.pack(pady=2)
        
        # 第二組輸出
        group2_frame = ttk.Frame(output_frame)
        group2_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        output_label2 = ttk.Label(group2_frame, text="第二組輸出結果：")
        output_label2.pack(anchor=tk.W)
        
        output_scroll2 = ttk.Scrollbar(group2_frame)
        output_scroll2.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_textbox2 = tk.Text(group2_frame, height=4, width=60, yscrollcommand=output_scroll2.set)
        self.output_textbox2.pack(fill=tk.BOTH, expand=True)
        output_scroll2.config(command=self.output_textbox2.yview)
        
        copy_button2 = ttk.Button(group2_frame, text="複製第二組資料", 
                                 command=lambda: self.copy_to_clipboard(self.output_textbox2))
        copy_button2.pack(pady=2)
        
        # 第三組輸出
        group3_frame = ttk.Frame(output_frame)
        group3_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        output_label3 = ttk.Label(group3_frame, text="逐行輸出 gameCode：")
        output_label3.pack(anchor=tk.W)
        
        output_scroll3 = ttk.Scrollbar(group3_frame)
        output_scroll3.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_textbox3 = tk.Text(group3_frame, height=4, width=60, yscrollcommand=output_scroll3.set)
        self.output_textbox3.pack(fill=tk.BOTH, expand=True)
        output_scroll3.config(command=self.output_textbox3.yview)
        
        copy_button3 = ttk.Button(group3_frame, text="複製第三組資料", 
                                 command=lambda: self.copy_to_clipboard(self.output_textbox3))
        copy_button3.pack(pady=2)
        
        # 第四組輸出
        group4_frame = ttk.Frame(output_frame)
        group4_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        output_label4 = ttk.Label(group4_frame, text="逐行輸出 gameName：")
        output_label4.pack(anchor=tk.W)
        
        output_scroll4 = ttk.Scrollbar(group4_frame)
        output_scroll4.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_textbox4 = tk.Text(group4_frame, height=4, width=60, yscrollcommand=output_scroll4.set)
        self.output_textbox4.pack(fill=tk.BOTH, expand=True)
        output_scroll4.config(command=self.output_textbox4.yview)
        
        copy_button4 = ttk.Button(group4_frame, text="複製第四組資料", 
                                 command=lambda: self.copy_to_clipboard(self.output_textbox4))
        copy_button4.pack(pady=2)
        
        # 第五組輸出
        group5_frame = ttk.Frame(output_frame)
        group5_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        output_label5 = ttk.Label(group5_frame, text="逐行輸出 imageUrl：")
        output_label5.pack(anchor=tk.W)
        
        output_scroll5 = ttk.Scrollbar(group5_frame)
        output_scroll5.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_textbox5 = tk.Text(group5_frame, height=4, width=60, yscrollcommand=output_scroll5.set)
        self.output_textbox5.pack(fill=tk.BOTH, expand=True)
        output_scroll5.config(command=self.output_textbox5.yview)
        
        copy_button5 = ttk.Button(group5_frame, text="複製第五組資料", 
                                 command=lambda: self.copy_to_clipboard(self.output_textbox5))
        copy_button5.pack(pady=2)
        
        # SQL輸出區域
        sql_output_frame = ttk.LabelFrame(self.main_frame, text="SQL輸出區域")
        sql_output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # SQL參數設定
        sql_params_frame = ttk.Frame(sql_output_frame)
        sql_params_frame.pack(fill=tk.X, padx=5, pady=5)

        # 遊戲供應商ID
        ttk.Label(sql_params_frame, text="providerId:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.provider_id_entry = ttk.Entry(sql_params_frame, width=10)
        self.provider_id_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)

        # 遊戲類別
        ttk.Label(sql_params_frame, text="category:").grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.category_entry = ttk.Entry(sql_params_frame, width=10)
        self.category_entry.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)

        # 自動轉帳
        ttk.Label(sql_params_frame, text="autotransfer:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.auto_transfer_entry = ttk.Entry(sql_params_frame, width=10)
        self.auto_transfer_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.auto_transfer_entry.insert(0, "0")  # 預設值

        # H5標誌
        ttk.Label(sql_params_frame, text="h5flag:").grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)
        self.h5_flag_entry = ttk.Entry(sql_params_frame, width=10)
        self.h5_flag_entry.grid(row=1, column=3, padx=5, pady=2, sticky=tk.W)
        self.h5_flag_entry.insert(0, "1")  # 預設值

        # 遊戲類型
        ttk.Label(sql_params_frame, text="gametype:").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        self.game_type_entry = ttk.Entry(sql_params_frame, width=10)
        self.game_type_entry.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        self.game_type_entry.insert(0, "10")  # 預設值

        # 生成SQL按鈕
        generate_sql_button = ttk.Button(sql_params_frame, text="生成SQL", command=self.generate_sql)
        generate_sql_button.grid(row=2, column=2, columnspan=2, padx=5, pady=2, sticky=tk.E)

        # SQL輸出框
        sql_scroll = ttk.Scrollbar(sql_output_frame)
        sql_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.sql_textbox = tk.Text(sql_output_frame, height=8, width=60, yscrollcommand=sql_scroll.set)
        self.sql_textbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        sql_scroll.config(command=self.sql_textbox.yview)

        # 複製SQL按鈕
        copy_sql_button = ttk.Button(sql_output_frame, text="複製SQL", 
                                command=lambda: self.copy_to_clipboard(self.sql_textbox))
        copy_sql_button.pack(pady=2)
        
        
        # 更新Canvas的捲軸區域
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def process_data(self):
        try:
            # 取得輸入框中的資料
            input_text = self.input_textbox.get("1.0", tk.END).strip()
            input_data = json.loads(input_text)  # 將字串轉換為 JSON
            
            # 第一組：取出所有 gameCode 並組成指定格式
            game_codes = "<<{}>>".format(">><<".join([item.get("gameCode", "") for item in input_data]))
            
            # 第二組：取出 gameCode 和 gameName 並組成新的 JSON
            game_list = [{"code": item.get("gameCode", ""), "name": item.get("gameName", "")} for item in input_data]
            
            # 第三組：逐行輸出 gameCode
            game_codes_lines = "\n".join([item.get("gameCode", "") for item in input_data])
            
            # 第四組：逐行輸出 gameName
            game_names_lines = "\n".join([item.get("gameName", "") for item in input_data])
            
            # 第五組：逐行輸出 imageUrl
            image_urls_lines = "\n".join([item.get("imageUrl", "") if item.get("imageUrl") is not None else "" for item in input_data])
            
            # 扁平化處理第二組資料
            flattened_game_list = json.dumps(game_list, separators=(',', ':'))
            
            # 將結果顯示在輸出框中
            self.output_textbox1.delete("1.0", tk.END)
            self.output_textbox1.insert(tk.END, game_codes)
            
            self.output_textbox2.delete("1.0", tk.END)
            self.output_textbox2.insert(tk.END, flattened_game_list)
            
            self.output_textbox3.delete("1.0", tk.END)
            self.output_textbox3.insert(tk.END, game_codes_lines)
            
            self.output_textbox4.delete("1.0", tk.END)
            self.output_textbox4.insert(tk.END, game_names_lines)
            
            self.output_textbox5.delete("1.0", tk.END)
            self.output_textbox5.insert(tk.END, image_urls_lines)
        except json.JSONDecodeError:
            messagebox.showerror("錯誤", "請輸入有效的 JSON 資料！")
        except Exception as e:
            messagebox.showerror("錯誤", f"發生錯誤：{e}")
    
    def copy_to_clipboard(self, output_textbox):
        # 將指定的輸出框內容複製到剪貼簿
        self.clipboard_clear()
        self.clipboard_append(output_textbox.get("1.0", tk.END).strip())
        self.update()  # 更新剪貼簿
    
    def on_frame_configure(self):
        # 更新捲軸區域
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        # 滑鼠滾輪滾動
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def generate_sql(self):
        try:
            # 取得輸入框中的資料
            input_text = self.input_textbox.get("1.0", tk.END).strip()
            json_data = json.loads(input_text)  # 將字串轉換為 JSON
            
            # 檢查是否有 result 鍵，如果有則只處理 result 部分
            if isinstance(json_data, dict) and 'result' in json_data:
                input_data = json_data['result']
            else:
                input_data = json_data  # 如果沒有 result 鍵，則使用整個 JSON
            
            # 取得自訂參數
            # 檢查必填欄位
            provider_id = self.provider_id_entry.get().strip()
            category = self.category_entry.get().strip()
            
            # 檢查必填欄位是否有值
            if not provider_id:
                messagebox.showerror("錯誤", "遊戲供應商ID為必填欄位！")
                return
            
            if not category:
                messagebox.showerror("錯誤", "遊戲類別為必填欄位！")
                return
            category = self.category_entry.get().strip() or "90"
            auto_transfer = self.auto_transfer_entry.get().strip() or "0"
            h5_flag = self.h5_flag_entry.get().strip() or "1"
            game_type = self.game_type_entry.get().strip() or "10"
            
            # 生成SQL語句
            sql_statements = []
            for item in input_data:
                game_code = item.get("gameCode", "")
                game_name = item.get("gameName", "")
                image_url = item.get("imageUrl", "")
                
                sql = (f"INSERT INTO public.t_game_provider_game(f_id, f_name, f_game_provider_id, "
                    f"f_category, f_auto_transfer, f_code, f_h5_flag, f_image_url, f_game_type) "
                    f"VALUES (nextval('seq_game_provider_game_id'), '{game_name}', {provider_id}, "
                    f"'{category}', {auto_transfer}, '{game_code}', {h5_flag}, '{image_url}', {game_type});")
                
                sql_statements.append(sql)
            
            # 將結果顯示在SQL輸出框中
            self.sql_textbox.delete("1.0", tk.END)
            self.sql_textbox.insert(tk.END, "\n".join(sql_statements))
        except json.JSONDecodeError:
            messagebox.showerror("錯誤", "請輸入有效的 JSON 資料！")
        except Exception as e:
            messagebox.showerror("錯誤", f"發生錯誤：{e}")
