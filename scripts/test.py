from pathlib import Path
import sys
import datetime

#-----------------------------準備-----------------------------------

if len(sys.argv) < 2:
    print("【エラー】ファイルのパスを指定してください。")
    sys.exit(0)  # プログラムを終了する ０は正常終了

source_file_path = Path(sys.argv[1])
directory_path_list = sys.argv[1].split("/")[:-1]
path_length = len(directory_path_list)

index_file_path = Path("/".join(directory_path_list) + "/index.html")

if not source_file_path.exists():
    print(f"【エラー】指定されたファイルが見つかりません: {source_file_path}")
    #fはpath型をstring型に自動で変えるために必要
    sys.exit(0)

today = datetime.date.today()

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
    "          <li><a href=\"\">ホーム</a></li>"
]

header_4 = [
    "        </ul>",
    "      </nav>",
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
        path_from_source_list = line.split("/")[:-1]
        if not len(path_from_source_list) == path_length:
            print("pathの長さが合いません")
            sys.exit(1)
        for i in range(path_length):
            if not path_from_source_list[i] == directory_path_list[i]:
                print("pathが合いません")
                sys.exit(1)
        if not line[0] in ["-"," "]:
            continue

        if line[0] == "-":
            with open(index_file_path, "w", encoding="utf-8") as index:
                #---------------------メタデータ-------------------------
                metadata = line.split(":")
                if not len(metadata) == 3:
                    print("メタデータの数が合いません")
                    sys.exit(1)
                title_list = metadata[1].split("/")
                title = title_list[path_length-2]
                if not len(title_list)-1 == path_length:
                    print("日本語タイトルの数が合いません")
                    sys.exit(1)
                description = metadata[2]

                #------------ヘッダー---------------------------------
                print(*header_1, sep="\n", end="", file=index)
                print(description, end="", file=index)
                print(hedaer_2, end="", file=index)
                print(title, end="", file=index)
                print(*header_3, sep="\n", file=index)
                for i in range(path_length-1):
                    print("          <li><a href=\"" + path_from_source_list[i] + "/\">" + title_list[i] + "</a></li>", file=index)
                print("          <li><span aria-current=\"page\">" + title + "</span></li>", file=index)
                # 各行を読んで本文をリストに収めながら、indexに目次を書き込んでいく。
                # 一番下まで行ったらリストを書き込み、最後にフッターを足す。