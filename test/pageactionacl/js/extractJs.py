import re
import os
import glob
import sys

def extract_func_urls_from_js(js_file_path):
    """從 JS 檔案中提取所有以 /func 開頭的 URL"""
    try:
        with open(js_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 使用正則表達式匹配 '' 或 `` 中的 /func 開頭的 URL
        # 匹配單引號包裹的 URL
        single_quote_pattern = r"'(/func[^']*?)'"
        # 匹配反引號包裹的 URL
        backtick_pattern = r"`(/func[^`]*?)`"
        # 匹配雙引號包裹的 URL
        double_quote_pattern = r'"(/func[^"]*?)"'
        
        # 提取所有匹配的 URL
        single_quote_urls = re.findall(single_quote_pattern, content)
        backtick_urls = re.findall(backtick_pattern, content)
        double_quote_urls = re.findall(double_quote_pattern, content)
        
        # 合併結果並去重
        all_urls = list(set(single_quote_urls + backtick_urls + double_quote_urls))
        
        return all_urls
    except Exception as e:
        print(f"處理檔案 {js_file_path} 時發生錯誤: {e}")
        return []

def generate_sql_for_urls(urls, file_name):
    """為提取的 URL 生成 SQL 插入語句"""
    sql_template = "INSERT INTO t_page_action_acl (f_id, f_url, f_acl, f_clazz_path, f_roles, f_type, f_check_obj_permission, f_entity_id) VALUES (nextval('seq_page_action_acl_id'), '{url}', '', '', 'ROLE_ADMIN,ROLE_MANAGER,ROLE_GROUP_ADMIN', 20, 0, entity_id);"
    
    sql_statements = []
    for url in urls:
        sql = sql_template.format(url=url)
        sql_statements.append(sql)
    
    return sql_statements

def process_js_files(directory_path=None, file_pattern='*.js'):
    """處理目錄中所有符合模式的 JS 檔案"""
    # 如果沒有指定目錄，使用腳本所在的目錄
    if directory_path is None:
        directory_path = os.path.dirname(os.path.abspath(__file__))
    
    js_files = glob.glob(os.path.join(directory_path, file_pattern))
    print(f"找到 {len(js_files)} 個 JS 檔案在路徑 '{directory_path}' 中")
    
    if len(js_files) == 0:
        print(f"在 '{directory_path}' 中沒有找到 '{file_pattern}' 檔案")
        return {}
    
    results = {}
    total_urls = 0
    
    for js_file in js_files:
        file_name = os.path.basename(js_file)
        print(f"正在處理檔案: {file_name}")
        urls = extract_func_urls_from_js(js_file)
        
        if urls:
            print(f"  在 {file_name} 中找到 {len(urls)} 個 URL")
            total_urls += len(urls)
            sql_statements = generate_sql_for_urls(urls, file_name)
            results[file_name] = sql_statements
        else:
            print(f"  在 {file_name} 中沒有找到 /func 開頭的 URL")
    
    print(f"總共找到 {total_urls} 個 /func 開頭的 URL")
    return results

def main():
    # 獲取腳本所在的目錄
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"腳本所在目錄: {script_dir}")
    
    # 處理腳本所在目錄中的 JS 檔案
    results = process_js_files(script_dir)
    
    # 如果沒有結果，嘗試在腳本所在目錄的子目錄中查找
    if not results:
        for root, dirs, files in os.walk(script_dir):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                print(f"\n嘗試在子目錄 '{dir_path}' 中查找 JS 檔案...")
                results = process_js_files(dir_path)
                if results:
                    break
            if results:
                break
    
    # 輸出結果
    if results:
        for file_name, sql_statements in results.items():
            print(f"\n檔案: {file_name}")
            print(f"找到 {len(sql_statements)} 個 /func 開頭的 URL")
            print("生成的 SQL 語句:")
            for sql in sql_statements:
                print(sql)
            print("-" * 80)
        
        # 將結果寫入檔案
        output_file = os.path.join(script_dir, "func_urls_sql.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            for file_name, sql_statements in results.items():
                f.write(f"\n檔案: {file_name}\n")
                f.write(f"找到 {len(sql_statements)} 個 /func 開頭的 URL\n")
                f.write("生成的 SQL 語句:\n")
                for sql in sql_statements:
                    f.write(f"{sql}\n")
                f.write("-" * 80 + "\n")
        print(f"\n結果已保存到: {output_file}")
    else:
        print("\n沒有找到任何包含 /func 開頭 URL 的 JS 檔案")
        print("你可以嘗試以下操作:")
        print("1. 確認 JS 檔案的位置是否正確")
        print("2. 檢查 JS 檔案中是否有以 /func 開頭的 URL")
        print("3. 將 JS 檔案放在與此 Python 程式相同的資料夾中")

# 示例用法
if __name__ == "__main__":
    print("開始執行 URL 提取程式...")
    main()
