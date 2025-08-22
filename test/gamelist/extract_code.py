import json

def extract_codes():
    # 讓使用者輸入JSON資料
    user_input = input("請輸入JSON資料: ")
    
    try:
        # 解析JSON
        data = json.loads(user_input)
        
        # 提取所有code並用<<>>包起來
        result = ''.join([f"<<{item['code']}>>" for item in data])
        
        print(f"結果: {result}")
        
    except json.JSONDecodeError:
        print("輸入的不是有效的JSON格式，請檢查格式")
    except KeyError:
        print("JSON中缺少'code'欄位")
    except Exception as e:
        print(f"發生錯誤: {e}")

# 執行函數
extract_codes()

