from pathlib import Path
import sys

if len(sys.argv) < 2:
    print("【エラー】ファイルのパスを指定してください。")
    sys.exit(0)  # プログラムを終了する ０は正常終了

source_file_path = Path(sys.argv[1])
index_file_path = Path(sys.argv[2])

if not source_file_path.exists():
    print(f"【エラー】指定されたファイルが見つかりません: {source_file_path}")#fはpath型をstring型に自動で変えるために必要
    sys.exit(0)

with open(source_file_path, mode="r", encoding="utf-8") as f:
    for line in f:
        print("これから "+line+" で作業する")
        if "-" not in line:
            with open(index_file_path, "w", encoding="utf-8") as file:
                file.write("test")