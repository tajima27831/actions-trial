from pathlib import Path
import sys

if len(sys.argv) < 2:
    print("【エラー】ファイルのパスを指定してください。")
    sys.exit(1)  # プログラムを終了する

file_path = Path(sys.argv[1])

# 3. 指定されたファイルが実際に存在するかチェック
if not file_path.exists():
    print(f"【エラー】指定されたファイルが見つかりません: {file_path}")
    sys.exit(1)

with open(file_path, mode="r", encoding="utf-8") as f:
    for line in f:
        print(line)