import re
import csv
from typing import List, Set
from datetime import datetime

def read_sql_acls(filename: str) -> List[str]:
    acl_list = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                matches = re.findall(r"'(ACL_[^']*)'", line)
                acl_list.extend(matches)
        return acl_list
    except Exception as e:
        print(f"Error reading SQL file: {e}")
        return []

def read_csv_acls(filename: str) -> List[str]:
    acl_list = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row and row[0].startswith("ACL_"):
                    acl_list.append(row[0].strip('"'))
        return acl_list
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def compare_and_save_results(sql_acls: List[str], csv_acls: List[str], output_file: str) -> None:
    sql_set = set(sql_acls)
    csv_set = set(csv_acls)
    
    only_in_sql = sql_set - csv_set
    only_in_csv = csv_set - sql_set
    common = sql_set & csv_set

    # 準備輸出內容
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_lines = [
        "ACL 比較結果報告",
        f"產生時間: {current_time}",
        f"\n檔案統計:",
        f"SQL 檔案中總共有: {len(sql_set)} 個 ACL",
        f"CSV 檔案中總共有: {len(csv_set)} 個 ACL",
        f"兩者共同擁有: {len(common)} 個 ACL",
        f"\n差異分析:"
    ]

    if only_in_sql:
        output_lines.append(f"\n只在 SQL 檔案中的 ACL ({len(only_in_sql)}):")
        for acl in sorted(only_in_sql):
            output_lines.append(f"+ {acl}")
    
    if only_in_csv:
        output_lines.append(f"\n只在 CSV 檔案中的 ACL ({len(only_in_csv)}):")
        for acl in sorted(only_in_csv):
            output_lines.append(f"- {acl}")

    output_lines.append("\n完整 ACL 列表:")
    output_lines.append("\nSQL 檔案中的 ACL:")
    for acl in sorted(sql_set):
        output_lines.append(acl)
    
    output_lines.append("\nCSV 檔案中的 ACL:")
    for acl in sorted(csv_set):
        output_lines.append(acl)

    # 寫入檔案
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
        print(f"\n結果已儲存到: {output_file}")
    except Exception as e:
        print(f"Error writing to output file: {e}")

    # 同時在控制台顯示主要結果
    print("\n=== 比較結果摘要 ===")
    print(f"SQL 檔案中總共有: {len(sql_set)} 個 ACL")
    print(f"CSV 檔案中總共有: {len(csv_set)} 個 ACL")
    print(f"兩者共同擁有: {len(common)} 個 ACL")
    print(f"只在 SQL 中: {len(only_in_sql)} 個")
    print(f"只在 CSV 中: {len(only_in_csv)} 個")

def main():
    # 設定檔案名稱
    sql_file = 'acl.sql'
    csv_file = 'acl.csv'
    output_file = f'acl_comparison_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

    # 讀取檔案
    sql_acls = read_sql_acls(sql_file)
    csv_acls = read_csv_acls(csv_file)
    
    # 比較並儲存結果
    compare_and_save_results(sql_acls, csv_acls, output_file)

if __name__ == "__main__":
    main()
