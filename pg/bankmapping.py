import csv
import json
import os

##資料範例參考/data/bankmappingpy/ 底下檔案
def process_csv_to_json(csv_file_path):
    # 創建一個字典來存儲結果
    result = {}
    
    # 讀取 CSV 檔案
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # 跳過標題行
        next(csv_reader)
        
        # 處理每一行
        for row in csv_reader:
            if len(row) >= 3:
                bank_name = row[0]
                bank_codes = row[1]
                provider_code = row[2]
                
                # 如果 bank_codes 不為空，處理它
                if bank_codes:
                    # 用分號分割 bank_codes
                    bank_code_list = bank_codes.split(';')
                    
                    # 將每個 bank_code 映射到 provider_code
                    for bank_code in bank_code_list:
                        # 去除可能的空格
                        bank_code = bank_code.strip()
                        if bank_code:  # 確保 bank_code 不是空字串
                            result[bank_code] = provider_code
    
    # 將結果轉換為 JSON 字串並返回
    return json.dumps(result, indent=2)

# 設定輸入檔案路徑
csv_file_path = 'cmnagaewallet.csv'

# 生成輸出檔案名稱（使用原始檔名 + .json）
base_name = os.path.splitext(csv_file_path)[0]  # 取得不含副檔名的檔案名稱
output_file_path = f"{base_name}.json"

# 處理 CSV 並轉換為 JSON
json_result = process_csv_to_json(csv_file_path)

# 輸出到檔案
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_result)

print(f"JSON 檔案已生成: {output_file_path}")
print("JSON 內容預覽:")
print(json_result[:500] + "...")  # 只顯示前 500 個字符
