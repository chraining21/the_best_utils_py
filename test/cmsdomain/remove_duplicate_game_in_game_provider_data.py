import json
import os

def read_file(file_path):
    """從檔案讀取資料"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"讀取檔案 {file_path} 時發生錯誤: {e}")
        return ""

def write_file(file_path, content):
    """將資料寫入檔案"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"寫入檔案 {file_path} 時發生錯誤: {e}")
        return False

def remove_codes_from_formats(codes_to_remove, format1_data, format2_data):
    """
    根據提供的 codes 列表，從兩種格式的資料中移除對應的 code
    
    Args:
        codes_to_remove: 要移除的 code 列表，格式如 "118,128,143,147"
        format1_data: 格式一的資料，如 "<<61>><<62>><<63>><<66>><<72>>"
        format2_data: 格式二的資料，JSON 字串，如 '[{"code":"61","name":"Dragon & Tiger"},...]'
    
    Returns:
        tuple: (處理後的格式一資料, 處理後的格式二資料)
    """
    # 將 codes_to_remove 轉換為列表
    if isinstance(codes_to_remove, str):
        codes_list = [code.strip() for code in codes_to_remove.split(',')]
    else:
        codes_list = codes_to_remove
    
    # 處理格式一：<<61>><<62>><<63>><<66>><<72>>
    processed_format1 = format1_data
    for code in codes_list:
        # 構建模式，匹配 <<code>>
        pattern = f"<<{code}>>"
        # 從格式一中移除匹配的 code
        processed_format1 = processed_format1.replace(pattern, "")
    
    # 處理格式二：JSON 格式的物件列表
    try:
        # 將 JSON 字串轉換為 Python 物件
        if isinstance(format2_data, str):
            json_data = json.loads(format2_data)
        else:
            json_data = format2_data
        
        # 過濾掉 code 在 codes_list 中的物件
        filtered_json_data = [item for item in json_data if item.get("code") not in codes_list]
        
        # 將過濾後的 Python 物件轉換回 JSON 字串，保持格式美觀
        processed_format2 = json.dumps(filtered_json_data, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        print("格式二的資料不是有效的 JSON 格式")
        processed_format2 = format2_data
    except Exception as e:
        print(f"處理格式二資料時發生錯誤: {e}")
        processed_format2 = format2_data
    
    return processed_format1, processed_format2

def main():
    # 檔案路徑設定 - 你可以直接修改這裡的檔名
    provider_name = "prg"
    codes_file = "codes_to_remove_"+provider_name+".txt"  # 包含要移除的 code 列表的檔案
    format1_file = "format1_data_"+provider_name+".txt"   # 包含格式一資料的檔案
    format2_file = "format2_data_"+provider_name+".json"  # 包含格式二資料的檔案

    # 輸出檔案路徑
    output_format1_file = provider_name + "processed_format1.txt"
    output_format2_file = provider_name + "processed_format2.json"
    summary_file = provider_name + "processing_summary.txt"
    
    # 檢查檔案是否存在
    missing_files = []
    for file_path in [codes_file, format1_file, format2_file]:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"找不到以下檔案: {', '.join(missing_files)}")
        return
    
    # 讀取檔案內容
    codes_to_remove = read_file(codes_file)
    format1_data = read_file(format1_file)
    format2_data = read_file(format2_file)
    
    # 處理資料
    processed_format1, processed_format2 = remove_codes_from_formats(codes_to_remove, format1_data, format2_data)
    
    # 將處理結果寫入檔案
    write_file(output_format1_file, processed_format1)
    write_file(output_format2_file, processed_format2)
    
    # 寫入處理摘要
    summary_content = f"""處理摘要:
要移除的 code: {codes_to_remove}

格式一原始資料: {format1_data}
格式一處理後: {processed_format1}

格式二原始資料檔案: {format2_file}
格式二處理後檔案: {output_format2_file}
"""
    write_file(summary_file, summary_content)
    
    # 輸出處理結果
    print(f"\n處理完成！")
    print(f"格式一處理結果已保存到: {output_format1_file}")
    print(f"格式二處理結果已保存到: {output_format2_file}")
    print(f"處理摘要已保存到: {summary_file}")

if __name__ == "__main__":
    main()
