import json
import csv
import os

def process_bank_mapping(json_file_path, csv_file_path, output_csv_path):
    # 讀取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        bank_code_map = json.load(json_file)
    
    # 讀取CSV文件
    rows = []
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)  # 讀取標題行
        headers.append('mapping code cronos(midas)')  # 添加新列標題
        rows.append(headers)
        
        # 處理每一行
        for row in csv_reader:
            bank_code = row[0] if row[0] else ""  # 獲取bank code並轉為小寫
            mapping_code = bank_code_map.get(bank_code, "")  # 在JSON中查找對應的值
            row.append(mapping_code)  # 添加匹配到的值或空字串
            rows.append(row)
    
    # 寫入新的CSV文件
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerows(rows)
    
    print(f"處理完成！新文件已保存為: {output_csv_path}")
    print(f"總共處理了 {len(rows) - 1} 行數據")

# 使用示例
if __name__ == "__main__":
    servername = "cmnaga"
    json_file_path = servername + "mapping.json"  # 你的JSON文件路徑
    csv_file_path = servername+" bank.csv"     # 你的CSV文件路徑
    output_csv_path = servername + "_bank_list_with_mapping.csv"  # 輸出文件路徑
    
    process_bank_mapping(json_file_path, csv_file_path, output_csv_path)
