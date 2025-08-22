import json
import sys

print("請貼上JSON資料，完成後按 Ctrl+D (Unix/Mac) 或 Ctrl+Enter (Windows):")

# 一次讀取所有輸入
json_data = sys.stdin.read()

try:
    # 解析JSON
    data = json.loads(json_data)

    # 提取gameCode和gameName，並重新格式化
    formatted_array = []
    for i, game in enumerate(data['result'], 1):
        formatted_array.append({
            "code": str(i),
            "name": game['gameName']
        })

    # 將格式化後的陣列轉為JSON字串
    formatted_json = json.dumps(formatted_array)

    # 提取code並以特定格式輸出
    codes = [item['code'] for item in formatted_array]
    formatted_codes = "<<" + ">><<".join(codes) + ">>"

    # 將兩種格式寫入檔案
    with open('game_data.txt', 'w') as file:
        file.write(formatted_json + "\n\n")
        file.write(formatted_codes)

    print("\n處理完成，結果已寫入 game_data.txt")
    print("\n格式化陣列:")
    print(formatted_json)
    print("\n格式化代碼:")
    print(formatted_codes)

except json.JSONDecodeError:
    print("輸入的JSON格式不正確，請檢查後重試。")
except KeyError as e:
    print(f"無法找到必要的鍵: {e}")
except Exception as e:
    print(f"發生錯誤: {e}")
