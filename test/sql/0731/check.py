import csv
import json,os

def check_payoutType(file_path):
    payoutType_values = {}
    error_rows = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row_num, row in enumerate(csv_reader, start=2):  # Start from 2 to account for header row
            try:
                # 處理JSON中的雙引號轉義問題
                f_data_raw = row['f_data']
                
                # 解析JSON
                data = json.loads(f_data_raw)
                
                # 檢查payoutType的值
                payoutType = data.get("reward", {}).get("payoutType")
                
                if payoutType not in payoutType_values:
                    payoutType_values[payoutType] = 0
                payoutType_values[payoutType] += 1
                
            except Exception as e:
                error_rows.append((row_num, str(e)))
    
    return payoutType_values, error_rows

# 執行函數並輸出SQL
script_dir = os.path.dirname(os.path.abspath(__file__))
# 執行檢查
csv_file_name = "bbb.csv"
file_path = os.path.join(script_dir, csv_file_name)
payoutType_values, error_rows = check_payoutType(file_path)

# 顯示結果
print("PayoutType值的分佈：")
for value, count in payoutType_values.items():
    print(f"  payoutType = {value}: {count}筆資料")

if error_rows:
    print("\n解析失敗的行數：")
    for row_num, error in error_rows:
        print(f"  第{row_num}行: {error}")
