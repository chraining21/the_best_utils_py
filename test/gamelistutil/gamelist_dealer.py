import tkinter as tk
from tkinter import messagebox, ttk
import json
from collections import defaultdict
from datetime import datetime

class GameProcessorFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        # 使用grid佈局而不是pack，以確保更精確的控制
        self.grid(sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 創建上下分割的面板
        self.paned_window = ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.paned_window.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # 創建輸入區域 - 左右分割 (減小權重，讓輸入框不那麼高)
        self.input_frame = ttk.LabelFrame(self.paned_window, text="遊戲資料輸入")
        self.paned_window.add(self.input_frame, weight=1)  # 權重從2改為1
        
        # 創建水平分割面板
        self.h_paned = ttk.PanedWindow(self.input_frame, orient=tk.HORIZONTAL)
        self.h_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 創建第一個輸入區域 (menuList)
        self.input1_frame = ttk.LabelFrame(self.h_paned, text="第一組資料 (menuList)")
        self.h_paned.add(self.input1_frame, weight=1)
        
        # 創建第一個輸入文本框和滾動條
        self.input1_text_frame = ttk.Frame(self.input1_frame)
        self.input1_text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.input1_scrollbar = ttk.Scrollbar(self.input1_text_frame)
        self.input1_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 設置文本框的高度，限制其顯示的行數
        self.input1_text = tk.Text(self.input1_text_frame, yscrollcommand=self.input1_scrollbar.set, height=10)
        self.input1_text.pack(fill=tk.BOTH, expand=True)
        self.input1_scrollbar.config(command=self.input1_text.yview)
        
        # 創建第二個輸入區域 (result)
        self.input2_frame = ttk.LabelFrame(self.h_paned, text="第二組資料 (result)")
        self.h_paned.add(self.input2_frame, weight=1)
        
        # 創建第二個輸入文本框和滾動條
        self.input2_text_frame = ttk.Frame(self.input2_frame)
        self.input2_text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.input2_scrollbar = ttk.Scrollbar(self.input2_text_frame)
        self.input2_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 設置文本框的高度，限制其顯示的行數
        self.input2_text = tk.Text(self.input2_text_frame, yscrollcommand=self.input2_scrollbar.set, height=10)
        self.input2_text.pack(fill=tk.BOTH, expand=True)
        self.input2_scrollbar.config(command=self.input2_text.yview)
        
        # 創建按鈕框架
        self.button_frame = ttk.Frame(self.input_frame)
        self.button_frame.pack(fill=tk.X, pady=5)
        
        # 創建處理按鈕
        self.process_button = ttk.Button(self.button_frame, text="處理遊戲列表", command=self.process_game_lists)
        self.process_button.pack(side=tk.LEFT, padx=5)
        
        # 創建清除按鈕
        self.clear_button = ttk.Button(self.button_frame, text="清除輸入", command=self.clear_input)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # 創建結果區域 - 使用grid佈局，增加權重讓結果區域更大
        self.result_frame = ttk.LabelFrame(self.paned_window, text="處理結果")
        self.paned_window.add(self.result_frame, weight=2)  # 權重從1改為2
        
        # 配置結果框架的grid佈局
        self.result_frame.grid_rowconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(1, weight=0)  # 按鈕行不需要擴展
        self.result_frame.grid_columnconfigure(0, weight=1)
        
        # 創建結果文本框和滾動條
        self.result_text_frame = ttk.Frame(self.result_frame)
        self.result_text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.result_scrollbar = ttk.Scrollbar(self.result_text_frame)
        self.result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(self.result_text_frame, yscrollcommand=self.result_scrollbar.set)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_scrollbar.config(command=self.result_text.yview)
        
        # 創建按鈕框架 - 使用grid佈局
        self.result_button_frame = ttk.Frame(self.result_frame)
        self.result_button_frame.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        # 創建複製結果按鈕
        self.copy_button = ttk.Button(self.result_button_frame, text="複製處理結果", command=self.copy_result)
        self.copy_button.pack(side=tk.LEFT, padx=5)
        
        # 創建複製壓縮JSON按鈕
        self.copy_minified_button = ttk.Button(self.result_button_frame, text="複製壓縮JSON", command=self.copy_minified_json)
        self.copy_minified_button.pack(side=tk.LEFT, padx=5)
    
    def process_game_lists(self):
        """從輸入框處理遊戲列表資料"""
        # 獲取輸入文本
        json1_text = self.input1_text.get("1.0", tk.END).strip()
        json2_text = self.input2_text.get("1.0", tk.END).strip()
        
        if not json2_text:
            messagebox.showwarning("警告", "請至少在第二個輸入框中輸入JSON資料")
            return
        
        try:
            # 解析JSON資料
            json2 = json.loads(json2_text)
            games2 = json2.get("result", [])
            
            self.log_message(f"第二組資料包含 {len(games2)} 個遊戲")
            
            # 如果第一個輸入為空，創建一個新的結構
            if not json1_text:
                self.log_message("第一組資料為空，將創建新的資料結構")
                json1 = {"menuList": []}
                games1 = []
            else:
                json1 = json.loads(json1_text)
                games1 = json1.get("menuList", [])
                self.log_message(f"第一組資料包含 {len(games1)} 個遊戲")
            
            # 如果第一組為空，直接使用第二組的所有遊戲
            if not games1:
                new_items = []
                for i, game2 in enumerate(games2, start=1):
                    # 將第二組的項目轉換為第一組的格式
                    new_item = {
                        "type": 101,  # 使用默認值
                        "imgUrl": game2.get("imageUrl", ""),
                        "status": 10,  # 使用默認值
                        "gameURL": "-1",  # 使用默認值
                        "category": game2.get("category", "").lower(),
                        "gameCode": game2.get("gameCode", ""),
                        "gameName": game2.get("gameName", ""),
                        "modifier": "justinadmin",  # 使用默認值
                        "position": i,  # 從1開始遞增
                        "providerId": 101,  # 使用默認值
                        "subCategory": ["new"],  # 使用默認值
                        "modifiedTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 使用當前時間
                        "rotationType": 3  # 使用默認值
                    }
                    new_items.append(new_item)
                
                self.log_message(f"創建了 {len(new_items)} 個新遊戲")
                json1["menuList"] = new_items
                
                # 將結果轉換為JSON字符串
                result_json = json.dumps(json1, ensure_ascii=False, indent=4)
                
                # 顯示結果
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, result_json)
                
                # 顯示處理摘要
                # 創建處理摘要訊息
                summary = "處理完成！\n"
                summary += "-" * 30 + "\n"
                summary += f"原始第一組遊戲數量: 0\n"
                summary += f"原始第二組遊戲數量: {len(games2)}\n"
                summary += f"創建的遊戲數量: {len(new_items)}\n"
                summary += f"最終遊戲數量: {len(new_items)}"

                # 使用 messagebox 顯示處理摘要
                messagebox.showinfo("處理完成", summary)
                return
            
            # 創建第二組的gameCode和gameName的映射，用於快速查找
            games2_map = {}
            for game in games2:
                if "gameCode" in game and "gameName" in game:
                    key = (game["gameCode"].lower(), game["gameName"].lower())
                    games2_map[key] = game
                else:
                    self.log_message(f"警告: 第二組資料中有遊戲缺少 gameCode 或 gameName")
            
            # 過濾第一組中的項目，只保留在第二組中存在的項目
            filtered_games1 = []
            removed_games = []
            invalid_games = []
            
            for game1 in games1:
                if "gameCode" in game1 and "gameName" in game1:
                    game1_key = (game1["gameCode"].lower(), game1["gameName"].lower())
                    if game1_key in games2_map:
                        filtered_games1.append(game1)
                    else:
                        removed_games.append(game1)
                else:
                    invalid_games.append(game1)
                    self.log_message(f"警告: 第一組資料中有遊戲缺少 gameCode 或 gameName")
            
            # 重新排序過濾後的遊戲列表
            for i, game in enumerate(filtered_games1, start=1):
                game["position"] = i
            
            self.log_message(f"保留 {len(filtered_games1)} 個遊戲，移除 {len(removed_games)} 個遊戲，無效 {len(invalid_games)} 個遊戲")
            self.log_message(f"已重新排序保留的遊戲，position從1到{len(filtered_games1)}")
            
            # 找出第二組中不在第一組的項目
            games1_map = {}
            for game in filtered_games1:
                if "gameCode" in game and "gameName" in game:
                    key = (game["gameCode"].lower(), game["gameName"].lower())
                    games1_map[key] = game
            
            new_items = []
            
            for game2 in games2:
                if "gameCode" in game2 and "gameName" in game2:
                    game2_key = (game2["gameCode"].lower(), game2["gameName"].lower())
                    if game2_key not in games1_map:
                        # 將第二組的項目轉換為第一組的格式
                        new_position = len(filtered_games1) + len(new_items) + 1
                        new_item = {
                            "type": 101,  # 使用默認值
                            "imgUrl": game2.get("imageUrl", ""),
                            "status": 10,  # 使用默認值
                            "gameURL": "-1",  # 使用默認值
                            "category": game2.get("category", "").lower(),
                            "gameCode": game2.get("gameCode", ""),
                            "gameName": game2.get("gameName", ""),
                            "modifier": "justinadmin",  # 使用默認值
                            "position": new_position,  # 從過濾後列表的最後一個position開始遞增
                            "providerId": 101,  # 使用默認值
                            "subCategory": ["new"],  # 使用默認值
                            "modifiedTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 使用當前時間
                            "rotationType": 3  # 使用默認值
                        }
                        new_items.append(new_item)
            
            self.log_message(f"新增 {len(new_items)} 個遊戲，position從{len(filtered_games1)+1}到{len(filtered_games1)+len(new_items)}")
            
            # 合併過濾後的第一組和新項目
            result_games = filtered_games1 + new_items
            
            # 更新第一組的menuList
            json1["menuList"] = result_games
            
            # 將結果轉換為JSON字符串
            result_json = json.dumps(json1, ensure_ascii=False, indent=4)
            
            # 顯示結果
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, result_json)
            
            # 顯示處理摘要
            summary = "處理完成！\n"
            summary += "-" * 30 + "\n"
            summary += f"原始第一組遊戲數量: {len(games1)}\n"
            summary += f"原始第二組遊戲數量: {len(games2)}\n"
            summary += f"保留的遊戲數量: {len(filtered_games1)}\n"
            summary += f"移除的遊戲數量: {len(removed_games)}\n"
            summary += f"無效的遊戲數量: {len(invalid_games)}\n"
            summary += f"新增的遊戲數量: {len(new_items)}\n"
            summary += f"最終遊戲數量: {len(result_games)}"

            # 使用 messagebox 顯示處理摘要
            messagebox.showinfo("處理完成", summary)
            
        except json.JSONDecodeError as e:
            import traceback
            error_msg = f"JSON格式錯誤:\n{str(e)}\n\n{traceback.format_exc()}"
            self.log_message(error_msg)
            messagebox.showerror("錯誤", error_msg)
        except Exception as e:
            import traceback
            error_msg = f"處理時發生錯誤:\n{str(e)}\n\n{traceback.format_exc()}"
            self.log_message(error_msg)
            messagebox.showerror("錯誤", error_msg)
    
    def clear_input(self):
        """清除輸入框內容"""
        self.input1_text.delete("1.0", tk.END)
        self.input2_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)
    
    def copy_result(self):
        """複製結果到剪貼板"""
        result_text = self.result_text.get("1.0", tk.END).strip()
        if result_text:
            self.clipboard_clear()
            self.clipboard_append(result_text)
            self.update()  # 更新剪貼簿
            messagebox.showinfo("提示", "處理結果已複製到剪貼簿!")
        else:
            messagebox.showwarning("警告", "沒有可複製的結果")
    
    def copy_minified_json(self):
        """複製壓縮後的JSON到剪貼板"""
        result_text = self.result_text.get("1.0", tk.END).strip()
        if result_text:
            try:
                # 解析JSON文本
                json_obj = json.loads(result_text)
                # 將JSON對象轉換為壓縮格式（不使用縮進和空格）
                minified_json = json.dumps(json_obj, ensure_ascii=False, separators=(',', ':'))
                
                # 複製到剪貼板
                self.clipboard_clear()
                self.clipboard_append(minified_json)
                self.update()  # 更新剪貼簿
                
                # 顯示壓縮前後的大小比較
                original_size = len(result_text)
                minified_size = len(minified_json)
                reduction = (1 - minified_size / original_size) * 100 if original_size > 0 else 0
                
                messagebox.showinfo("提示", f"壓縮JSON已複製到剪貼簿!\n原始大小: {original_size} 字節\n壓縮後大小: {minified_size} 字節\n減少: {reduction:.2f}%")
            except json.JSONDecodeError:
                messagebox.showerror("錯誤", "無法解析JSON格式")
            except Exception as e:
                messagebox.showerror("錯誤", f"壓縮JSON時發生錯誤: {str(e)}")
        else:
            messagebox.showwarning("警告", "沒有可複製的結果")
    
    def log_message(self, message):
        """在結果文本框中添加日誌消息"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)  # 滾動到最後
