import json
import os
import sys

# 直接在代碼中指定 JSON 文件名
json_file = "spribe.json"  # 你可以改成你的文件名

# 創建輸出目錄名稱 (原檔名 + game_codes_output)
file_name_without_ext = os.path.splitext(json_file)[0]  # 獲取不含副檔名的檔名
output_dir = f"{file_name_without_ext}_game_codes_output"

# 讀取 JSON 文件
try:
    with open(json_file, 'r', encoding='utf-8') as file:
        games_data = json.load(file)
    print(f"成功讀取文件: {json_file}")
except FileNotFoundError:
    print(f"找不到文件: {json_file}")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"JSON 格式錯誤: {e}")
    sys.exit(1)
except Exception as e:
    print(f"讀取文件時發生錯誤: {e}")
    sys.exit(1)

# 按 category 分類遊戲
category_games = {}
for game in games_data:
    category = game.get('category')
    game_code = game.get('gameCode')
    if category and game_code:
        if category not in category_games:
            category_games[category] = []
        category_games[category].append(game_code)

# 如果沒有找到任何 category
if not category_games:
    print("沒有找到任何有效的 category 和 gameCode！")
    sys.exit(1)

# 創建輸出目錄
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"已創建輸出目錄: {output_dir}")

# 顯示找到的 category
print("\n找到以下 category:")
for category in sorted(category_games.keys()):
    print(f"- {category} (遊戲數量: {len(category_games[category])})")

# 為每個 category 創建文件
for category, game_codes in sorted(category_games.items()):
    filename = os.path.join(output_dir, f"{category}_game_codes.txt")
    game_codes_str = ','.join(game_codes)
    
    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write(f"Category: {category}\n")
        output_file.write(f"遊戲數量: {len(game_codes)}\n")
        output_file.write(f"Game Codes: {game_codes_str}\n")
    
    print(f"已保存 {category} 的遊戲代碼到文件: {filename}")

# 創建一個包含所有 category 的總文件
all_filename = os.path.join(output_dir, "all_categories_game_codes.txt")
with open(all_filename, 'w', encoding='utf-8') as all_output_file:
    for category, game_codes in sorted(category_games.items()):
        game_codes_str = ','.join(game_codes)
        all_output_file.write(f"Category: {category}\n")
        all_output_file.write(f"遊戲數量: {len(game_codes)}\n")
        all_output_file.write(f"Game Codes: {game_codes_str}\n")
        all_output_file.write("-" * 50 + "\n")

print(f"已保存所有 category 的遊戲代碼到文件: {all_filename}")
print(f"\n處理完成！所有文件已保存到 {output_dir} 目錄中。")
