import csv
import json
import os
import re

def process_csv_file(file_path):
    update_sql_list = []
    processed_ids = []  # 用來存儲被處理的ID
    
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            f_id = row['f_id']
            f_data_raw = row['f_data']
            
            try:
                # 解析JSON
                data = json.loads(f_data_raw)
                
                # 檢查payoutType是否為20，如果不是則跳過
                if data.get("reward", {}).get("payoutType") != "20":
                    continue
                
                # 處理settingList
                if "settingList" in data.get("reward", {}):
                    for item in data["reward"]["settingList"]:
                        for setting_key in ["setting1", "setting2", "setting3", "setting4", "setting5"]:
                            if setting_key in item and item[setting_key]:
                                # 將值除以100
                                try:
                                    value = float(item[setting_key])
                                    item[setting_key] = f"{value/100:.4f}"
                                except ValueError:
                                    # 如果無法轉換為浮點數，保持原值
                                    pass
                
                # 將修改後的JSON轉回字串，並處理引號問題
                modified_json = json.dumps(data, ensure_ascii=False)
                # 將JSON中的引號轉義為SQL中的格式
                escaped_json = modified_json.replace("'", "''")
                
                # 生成SQL更新語句
                sql = f"update t_menu_page_item set f_data = '{escaped_json}' where f_id = {f_id};"
                update_sql_list.append(sql)
                
                # 記錄被處理的ID
                processed_ids.append(f_id)
                
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON for f_id {f_id}: {e}")
                # 顯示問題位置附近的字元
                error_pos = e.pos
                start = max(0, error_pos - 20)
                end = min(len(f_data_raw), error_pos + 20)
                context = f_data_raw[start:end]
                print(f"問題上下文: ...{context}...")
                # 顯示問題字元的ASCII值
                if error_pos < len(f_data_raw):
                    problem_char = f_data_raw[error_pos]
                    print(f"問題字元: '{problem_char}', ASCII值: {ord(problem_char)}")
    
    return update_sql_list, processed_ids

# 執行函數並輸出SQL
script_dir = os.path.dirname(os.path.abspath(__file__))
    
# 設定CSV檔案的路徑（與程式碼在同一資料夾）
csv_file_name = "aaa.csv"
file_path = os.path.join(script_dir, csv_file_name)
sql_statements, processed_ids = process_csv_file(file_path)

# 輸出SQL語句到檔案
with open("update_queries.sql", "w", encoding="utf-8") as sql_file:
    for sql in sql_statements:
        sql_file.write(sql + "\n")

# 輸出被處理的ID到檔案
with open("processed_ids.txt", "w", encoding="utf-8") as id_file:
    id_file.write("處理的資料ID列表：\n")
    for f_id in processed_ids:
        id_file.write(f"{f_id}\n")

# 生成查詢SQL並輸出到檔案
if processed_ids:
    # 將ID列表轉成字符串，用逗號分隔
    ids_string = ','.join(processed_ids)
    select_sql = f"SELECT * FROM t_menu_page_item WHERE f_id IN ({ids_string});"
    
    with open("select_processed_ids.sql", "w", encoding="utf-8") as select_file:
        select_file.write(select_sql)
    
    print(f"查詢SQL已保存到 select_processed_ids.sql 檔案")

# 在終端顯示處理結果
print(f"已生成 {len(sql_statements)} 條SQL更新語句，並保存到 update_queries.sql 檔案")
print(f"處理的資料ID列表：{', '.join(processed_ids)}")
print(f"ID列表已保存到 processed_ids.txt 檔案")
