from pathlib import Path
import sys
import datetime

#-----------------------------準備-----------------------------------

if len(sys.argv) < 3:
    print("【エラー】ファイルのパスを指定してください。")
    sys.exit(0)  # プログラムを終了する ０は正常終了

source_file_path = Path(sys.argv[1])
index_file_path = Path(sys.argv[2])

if not source_file_path.exists():
    print(f"【エラー】指定されたファイルが見つかりません: {source_file_path}")
    #fはpath型をstring型に自動で変えるために必要
    sys.exit(0)

today = datetime.date.today()

path_list = sys.argv[1].split("/")

#--------------------------ヘッダー--------------------------------

header_1 = [
    "<!doctype html>",
    "<html lang=\"ja\">",
    "  <head>",
    "    <link rel=\"icon\" href=\"resources/images/diagram.jpg\" type=\"image/x-icon\"/>",
    "    <meta charset=\"UTF-8\"/>",
    "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>",
    "    <meta name=\"description\" content=\""
]

hedaer_2 = "\"/>\n    <title>"

header_3 = [
    "｜強迫的敗北主義反芻派</title>",
    "    <link href=\"resources/styles/common.css\" rel=\"stylesheet\"/>",
    "  </head>",
    "",
    "  <body>",
    "    <header>",
    "      <div class=\"site-name\">強迫的敗北主義反芻派</div>",
    "",
    "      <hr>",
    "",
    "      <nav aria-label=\"Breadcrumb\">",
    "        <ul class=\"breadcrumb\">",
    "          <li><a href=\"\">ホーム</a></li>",
    "          <li><a href=\"" + path_list[0] + "/\">"
]
# 上の階層の日本語のタイトルがパンくずリストのために要る
header_4 = [
    "",
    "      <div class=\"last-update\">このページの最終更新：<time datetime=\"" + today.strftime("%Y-%m-%d") + "\">" + today.strftime("%Y年%m月%d日") + "</time></div>",
    "",
    "      <nav>",
    "        このページの目次",
    "        <ul class=\"contents\">",
    "          <li>"
]

with open(source_file_path, mode="r", encoding="utf-8") as source:
    for line in source:
        if line=="":
            continue
        if not line[0] in ["-"," "]:
            continue

        if line[0] == "-":
            with open(index_file_path, "w", encoding="utf-8") as index:
                #---------------------メタデータ-------------------------
                metadata = line.split(":")
                if not len(metadata) == 3:
                    print("メタデータの異常")
                    sys.exit(1)
                title = metadata[1]
                description = metadata[2]

                #------------ヘッダー---------------------------------
                print(*header_1, sep="\n", end="", file=index)
                print(description, end="", file=index)
                print(hedaer_2, end="", file=index)
                print(title, end="", file=index)
                print(*header_3, sep="\n", end="", file=index)