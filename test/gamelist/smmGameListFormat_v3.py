import tkinter as tk
from tkinter import messagebox, ttk
import json

def process_data():
    try:
        # 取得輸入框中的資料
        input_text = input_textbox.get("1.0", tk.END).strip()
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
        output_textbox1.delete("1.0", tk.END)  # 清空第一組輸出框
        output_textbox1.insert(tk.END, game_codes)
        
        output_textbox2.delete("1.0", tk.END)  # 清空第二組輸出框
        output_textbox2.insert(tk.END, flattened_game_list)
        
        output_textbox3.delete("1.0", tk.END)  # 清空第三組輸出框
        output_textbox3.insert(tk.END, game_codes_lines)
        
        output_textbox4.delete("1.0", tk.END)  # 清空第四組輸出框
        output_textbox4.insert(tk.END, game_names_lines)
        
        output_textbox5.delete("1.0", tk.END)  # 清空第五組輸出框
        output_textbox5.insert(tk.END, image_urls_lines)
    except json.JSONDecodeError:
        messagebox.showerror("錯誤", "請輸入有效的 JSON 資料！")
    except Exception as e:
        messagebox.showerror("錯誤", f"發生錯誤：{e}")

def copy_to_clipboard(output_textbox):
    # 將指定的輸出框內容複製到剪貼簿
    root.clipboard_clear()
    root.clipboard_append(output_textbox.get("1.0", tk.END).strip())
    root.update()  # 更新剪貼簿
    # messagebox.showinfo("提示", "內容已複製到剪貼簿！")

def on_frame_configure(canvas):
    # 更新捲軸區域
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_mousewheel(event):
    # 滑鼠滾輪滾動
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# 建立主視窗
root = tk.Tk()
root.title("資料處理工具")
root.geometry("800x600")  # 設定初始大小

# 創建主Canvas和捲軸
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# 放置Canvas和捲軸
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 創建主框架放在Canvas上
main_frame = ttk.Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=main_frame, anchor="nw")

# 綁定事件
main_frame.bind("<Configure>", lambda e: on_frame_configure(canvas))
canvas.bind_all("<MouseWheel>", on_mousewheel)

# 輸入區域
input_frame = ttk.LabelFrame(main_frame, text="輸入區域")
input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# 輸入框標籤
input_label = ttk.Label(input_frame, text="請輸入 JSON 資料：")
input_label.pack(padx=5, pady=2)

# 輸入框和捲軸
input_scroll = ttk.Scrollbar(input_frame)
input_scroll.pack(side=tk.RIGHT, fill=tk.Y)
input_textbox = tk.Text(input_frame, height=10, width=60, yscrollcommand=input_scroll.set)
input_textbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
input_scroll.config(command=input_textbox.yview)

# 處理按鈕
process_button = ttk.Button(input_frame, text="處理資料", command=process_data)
process_button.pack(pady=5)

# 輸出區域
output_frame = ttk.LabelFrame(main_frame, text="輸出區域")
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# 第一組輸出
group1_frame = ttk.Frame(output_frame)
group1_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

output_label1 = ttk.Label(group1_frame, text="第一組輸出結果：")
output_label1.pack(anchor=tk.W)

output_scroll1 = ttk.Scrollbar(group1_frame)
output_scroll1.pack(side=tk.RIGHT, fill=tk.Y)
output_textbox1 = tk.Text(group1_frame, height=4, width=60, yscrollcommand=output_scroll1.set)
output_textbox1.pack(fill=tk.BOTH, expand=True)
output_scroll1.config(command=output_textbox1.yview)

copy_button1 = ttk.Button(group1_frame, text="複製第一組資料", command=lambda: copy_to_clipboard(output_textbox1))
copy_button1.pack(pady=2)

# 第二組輸出
group2_frame = ttk.Frame(output_frame)
group2_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

output_label2 = ttk.Label(group2_frame, text="第二組輸出結果：")
output_label2.pack(anchor=tk.W)

output_scroll2 = ttk.Scrollbar(group2_frame)
output_scroll2.pack(side=tk.RIGHT, fill=tk.Y)
output_textbox2 = tk.Text(group2_frame, height=4, width=60, yscrollcommand=output_scroll2.set)
output_textbox2.pack(fill=tk.BOTH, expand=True)
output_scroll2.config(command=output_textbox2.yview)

copy_button2 = ttk.Button(group2_frame, text="複製第二組資料", command=lambda: copy_to_clipboard(output_textbox2))
copy_button2.pack(pady=2)

# 第三組輸出
group3_frame = ttk.Frame(output_frame)
group3_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

output_label3 = ttk.Label(group3_frame, text="逐行輸出 gameCode：")
output_label3.pack(anchor=tk.W)

output_scroll3 = ttk.Scrollbar(group3_frame)
output_scroll3.pack(side=tk.RIGHT, fill=tk.Y)
output_textbox3 = tk.Text(group3_frame, height=4, width=60, yscrollcommand=output_scroll3.set)
output_textbox3.pack(fill=tk.BOTH, expand=True)
output_scroll3.config(command=output_textbox3.yview)

copy_button3 = ttk.Button(group3_frame, text="複製第三組資料", command=lambda: copy_to_clipboard(output_textbox3))
copy_button3.pack(pady=2)

# 第四組輸出
group4_frame = ttk.Frame(output_frame)
group4_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

output_label4 = ttk.Label(group4_frame, text="逐行輸出 gameName：")
output_label4.pack(anchor=tk.W)

output_scroll4 = ttk.Scrollbar(group4_frame)
output_scroll4.pack(side=tk.RIGHT, fill=tk.Y)
output_textbox4 = tk.Text(group4_frame, height=4, width=60, yscrollcommand=output_scroll4.set)
output_textbox4.pack(fill=tk.BOTH, expand=True)
output_scroll4.config(command=output_textbox4.yview)

copy_button4 = ttk.Button(group4_frame, text="複製第四組資料", command=lambda: copy_to_clipboard(output_textbox4))
copy_button4.pack(pady=2)

# 第五組輸出
group5_frame = ttk.Frame(output_frame)
group5_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

output_label5 = ttk.Label(group5_frame, text="逐行輸出 imageUrl：")
output_label5.pack(anchor=tk.W)

output_scroll5 = ttk.Scrollbar(group5_frame)
output_scroll5.pack(side=tk.RIGHT, fill=tk.Y)
output_textbox5 = tk.Text(group5_frame, height=4, width=60, yscrollcommand=output_scroll5.set)
output_textbox5.pack(fill=tk.BOTH, expand=True)
output_scroll5.config(command=output_textbox5.yview)

copy_button5 = ttk.Button(group5_frame, text="複製第五組資料", command=lambda: copy_to_clipboard(output_textbox5))
copy_button5.pack(pady=2)

# 更新Canvas的捲軸區域
canvas.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# 啟動主循環
root.mainloop()
