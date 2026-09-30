from pathlib import Path
import sys

if len(sys.argv) < 2:
    print("【エラー】ファイルのパスを指定してください。")
    sys.exit(0)  # プログラムを終了する ０は正常終了

file_path = Path(sys.argv[1])

if not file_path.exists():
    print(f"【エラー】指定されたファイルが見つかりません: {file_path}")
    sys.exit(0)

with open(file_path, mode="r", encoding="utf-8") as f:
    for line in f:
        print(line)