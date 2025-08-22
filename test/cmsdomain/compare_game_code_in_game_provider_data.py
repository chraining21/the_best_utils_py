import os

def read_codes_from_file(file_path, delimiter=','):
    """從文件中讀取 code，支援每行一個或用逗號分隔的格式"""
    codes = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            # 檢查內容是否包含分隔符
            if delimiter in content:
                # 如果包含分隔符，按分隔符分割
                for line in content.split('\n'):
                    for code in line.split(delimiter):
                        code = code.strip()
                        if code:  # 確保不添加空字符串
                            codes.add(code)
            else:
                # 如果不包含分隔符，按行分割
                for line in content.split('\n'):
                    line = line.strip()
                    if line:  # 確保不添加空行
                        codes.add(line)
        return codes
    except Exception as e:
        print(f"讀取文件 {file_path} 時發生錯誤: {e}")
        return set()

def compare_codes(file1_path, file2_path, output_path):
    """比較兩個文件中的 code 並輸出結果"""
    # 獲取文件名（不含路徑）
    file1_name = os.path.basename(file1_path)
    file2_name = os.path.basename(file2_path)
    
    # 檢查文件是否存在
    if not os.path.exists(file1_path):
        print(f"找不到文件: {file1_path}")
        return
    if not os.path.exists(file2_path):
        print(f"找不到文件: {file2_path}")
        return
    
    # 讀取 code
    codes1 = read_codes_from_file(file1_path)
    codes2 = read_codes_from_file(file2_path)
    
    # 找出共同的和獨有的 code
    common_codes = codes1.intersection(codes2)
    only_in_file1 = codes1 - codes2
    only_in_file2 = codes2 - codes1
    
    # 輸出結果
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # 寫入摘要
        output_file.write(f"比較結果摘要:\n")
        output_file.write(f"檔案1: {file1_name} (共 {len(codes1)} 個 code)\n")
        output_file.write(f"檔案2: {file2_name} (共 {len(codes2)} 個 code)\n")
        output_file.write(f"共同的 code: {len(common_codes)} 個\n")
        output_file.write(f"僅在 {file1_name} 中的 code: {len(only_in_file1)} 個\n")
        output_file.write(f"僅在 {file2_name} 中的 code: {len(only_in_file2)} 個\n\n")
        
        # 寫入共同的 code
        output_file.write(f"共同的 code ({len(common_codes)} 個):\n")
        output_file.write(','.join(sorted(common_codes)) + "\n\n")
        
        # 寫入僅在文件1中的 code
        output_file.write(f"僅在 {file1_name} 中的 code ({len(only_in_file1)} 個):\n")
        output_file.write(','.join(sorted(only_in_file1)) + "\n\n")
        
        # 寫入僅在文件2中的 code
        output_file.write(f"僅在 {file2_name} 中的 code ({len(only_in_file2)} 個):\n")
        output_file.write(','.join(sorted(only_in_file2)) + "\n")
    
    print(f"比較完成！結果已保存到 {output_path}")
    print(f"共同的 code: {len(common_codes)} 個")
    print(f"僅在 {file1_name} 中的 code: {len(only_in_file1)} 個")
    print(f"僅在 {file2_name} 中的 code: {len(only_in_file2)} 個")

# 主程序
if __name__ == "__main__":
    # 在這裡直接寫死檔名
    provider_name = "prg_crash"
    file1_path = "cmscode_"+provider_name+".txt"  # 第一個文件的路徑
    file2_path = "gameproviderdatacode_"+provider_name+".txt"  # 第二個文件的路徑
    output_path = file1_path.replace(".txt", "_vs_" + file2_path.replace(".txt", "") + ".txt")  # 結果輸出文件的路徑
    
    # 執行比較
    compare_codes(file1_path, file2_path, output_path)
