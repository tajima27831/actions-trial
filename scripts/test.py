from pathlib import Path
import sys
import datetime

#-----------------------------準備-----------------------------------

if len(sys.argv) < 2:
    print("【エラー】ファイルのパスを指定してください。")
    sys.exit(0)  # プログラムを終了する ０は正常終了

source_file_path = Path(sys.argv[1])
directory_path_list = sys.argv[1].split("/")[:-1]
path_length = len(directory_path_list)#ホームを含む

index_file_path = Path("/".join(directory_path_list) + "/index.html")

if not source_file_path.exists():
    print(f"【エラー】指定されたファイルが見つかりません: {source_file_path}")
    #fはpath型をstring型に自動で変えるために必要
    sys.exit(0)

today = datetime.date.today()

#--------------------------ヘッド--------------------------------

head_1 = [
    "<!doctype html>",
    "<html lang=\"ja\">",
    "  <head>",
    "    <link rel=\"icon\" href=\"resources/images/diagram.jpg\" type=\"image/x-icon\"/>",
    "    <meta charset=\"UTF-8\"/>",
    "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>",
    "    <link href=\"resources/styles/common.css\" rel=\"stylesheet\"/>"
]

head_metadata = [
]

head_2 = [
    "  </head>"
]

#--------------------------------ヘッダー-----------------------------------

header_1 = [
    "  <body>",
    "    <header>",
    "      <div class=\"site-name\">強迫的敗北主義反芻派</div>",
    "",
    "      <hr>",
    ""
]

header_breadcrumb = [
]

header_2 = [
    "",
    "      <div class=\"last-update\">このページの最終更新：<time datetime=\"" + today.strftime("%Y-%m-%d") + "\">" + today.strftime("%Y年%m月%d日") + "</time></div>",
    ""
]

header_contents = [
]

header_3 = [
    "    </header>"
]

#----------------------------------メイン------------------------------------

main_1 = [
]

#---------------------------------抽出---------------------------------------

with open(source_file_path, mode="r", encoding="utf-8") as source:
    for line in source:
        if line == "\n":
            continue

        #--------------------------------mdの一行目--------------------------------------
        if not line[0] in ["-"," "]:
            directory_path_from_source_list = line.split("/")[:-1]#ホームから始まる
            if not len(directory_path_from_source_list) == path_length:
                print("pathの長さが合いません")
                print(len(directory_path_from_source_list))
                sys.exit(1)
            for i in range(path_length):
                if not directory_path_from_source_list[i] == directory_path_list[i]:
                    print("pathが合いません")
                    sys.exit(1)

        #--------------------------------mdの三行目---------------------------------
        if line[0] == "-":
            #---------------------メタデータの取得-------------------------
            metadata = line.split(":")
            if not len(metadata) == 3:
                print("メタデータの数が合いません")
                sys.exit(1)
            title_list = metadata[1].split("/")[:-1]
            title = title_list[path_length-1]
            if not len(title_list) == path_length:
                print("日本語タイトルの数が合いません")
                sys.exit(1)
            description = metadata[2]

            head_metadata = [
                "    <meta name=\"description\" content=\"" + description + "\"/>",
                "    <title>" + title + "｜強迫的敗北主義反芻派</title>"
            ]

            header_breadcrumb.append("      <nav aria-label=\"Breadcrumb\">")
            header_breadcrumb.append("        <ul class=\"breadcrumb\">")
            header_breadcrumb.append("")
            for i in range(path_length-1):
                header_breadcrumb.append("          <li><a href=\"")
                for j in range(i):
                    header_breadcrumb.append(directory_path_from_source_list[j] + "/")
                header_breadcrumb.append("\">" + title_list[i] + "</a></li>")
            header_breadcrumb.append("          <li><span aria-current=\"page\">" + title + "</span></li>")
            header_breadcrumb.append("      </nav>")

        #-----------------------------本文---------------------------------------------
        # 各行を読んで本文をリストに収めながら、headerに目次を書き込んでいく。
        # 一番下まで行ったらリストを書き込み、最後にフッターを足す。

#--------------------------------------生成---------------------------------------------
with open(index_file_path, "w", encoding="utf-8") as result:
    print(*head_1, sep="\n", file=result)
    print(*head_metadata, sep="\n", file=result)
    print(*head_2, sep="\n", file=result)
    print(*header_1, sep="\n", file=result)
    print(*header_breadcrumb, sep="\n", file=result)
    print(*header_2, sep="\n", file=result)
    print(*header_contents, sep="\n", file=result)
    print(*header_3, sep="\n", file=result)
    print(*main_1, sep="\n", file=result)