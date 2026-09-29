import os
import re
from pathlib import Path


def parse_front_matter(content: str) -> tuple[dict, str]:
    """
    ファイル先頭のメタデータ (--- で囲まれたFront Matter) を解析する。
    戻り値: (メタデータの辞書, メタデータ除外後の本文テキスト)
    """
    metadata = {}
    body = content

    # --- で囲まれた範囲を正規表現で抽出
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        yaml_text, body = match.groups()
        for line in yaml_text.strip().split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                metadata[key.strip()] = val.strip()

    return metadata, body.strip()


def parse_item_content(text: str, heading_count: int, toc_items: list) -> tuple[str, int]:
    """
    箇条書きの各行の内容が『見出し』か『本文』かを判別してHTMLに変換する。
    見出しの場合は、IDの付与と目次用リスト (toc_items) への追加を行う。
    """
    text = text.strip()

    # 先頭の '#' の数に応じて <h1>〜<h6> を判定
    heading_match = re.match(r"^(#{1,6})\s+(.*)$", text)
    if heading_match:
        hashes, title_text = heading_match.groups()
        level = len(hashes)
        
        # 連番でユニークなIDを生成 (例: heading-1, heading-2)
        heading_count += 1
        heading_id = f"heading-{heading_count}"

        # 後で目次(TOC)を生成するために、見出し情報をリストに記録
        toc_items.append({
            "level": level,
            "text": title_text,
            "id": heading_id
        })

        # id属性を付与した見出しタグを返す
        html_tag = f'<h{level} id="{heading_id}">{title_text}</h{level}>'
        return html_tag, heading_count

    # '#' がない場合は通常の本文 (<p>) として返す
    return f"<p>{text}</p>", heading_count


def convert_nested_list_to_html(md_body: str) -> tuple[str, list]:
    """
    インデントされた箇条書きを <ul> / <li> の構造に変換し、
    同時に検出された見出し情報 (toc_items) を収集して返す。
    """
    lines = md_body.split("\n")
    html_lines = []
    stack = []         # インデントの深さを追跡するスタック
    toc_items = []     # 目次要素を貯めるリスト
    heading_count = 0  # 見出しのID用カウンタ

    for line in lines:
        if not line.strip():
            continue

        # 行頭のインデントと箇条書き記号 (-, *) を検出
        match = re.match(r"^(\s*)([-*])\s+(.*)$", line)
        if not match:
            # 箇条書き記号がない行の処理
            html_tag, heading_count = parse_item_content(line, heading_count, toc_items)
            html_lines.append(html_tag)
            continue

        indent, _, content = match.groups()
        indent_level = len(indent.replace("\t", "    "))

        # インデントの深さに合わせて <ul> の階層構造を調整
        if not stack:
            stack.append(indent_level)
            html_lines.append("<ul>")
        elif indent_level > stack[-1]:
            stack.append(indent_level)
            html_lines.append("<ul>")
        else:
            while stack and indent_level < stack[-1]:
                stack.pop()
                html_lines.append("  " * len(stack) + "</ul></li>")
            if stack and indent_level == stack[-1]:
                html_lines.append("  " * len(stack) + "</li>")

        # 項目のテキストを変換 (見出しならID付与とTOC追加が行われる)
        formatted_content, heading_count = parse_item_content(content, heading_count, toc_items)
        pad = "  " * len(stack)
        html_lines.append(f"{pad}<li>{formatted_content}")

    # 残った未閉じタグのクローズ処理
    while stack:
        stack.pop()
        pad = "  " * len(stack)
        html_lines.append(f"{pad}</li>\n{pad}</ul>")

    return "\n".join(html_lines), toc_items


def generate_toc_html(toc_items: list) -> str:
    """
    収集した見出し情報リストから、ページ冒頭に配置する目次 (TOC) のHTMLを構築する。
    """
    if not toc_items:
        return ""  # 見出しがなければ目次は作成しない

    toc_lines = [
        '<nav class="table-of-contents">',
        '  <h2>目次</h2>',
        '  <ul>'
    ]

    for item in toc_items:
        # 見出しレベルに応じたCSSクラスを付与 (インデント装飾用)
        level_class = f"toc-level-{item['level']}"
        # 目次リンク (<a href="#ID">タイトル</a>) の作成
        link = f'<a href="#{item["id"]}">{item["text"]}</a>'
        toc_lines.append(f'    <li class="{level_class}">{link}</li>')

    toc_lines.append('  </ul>')
    toc_lines.append('</nav>')

    return "\n".join(toc_lines)


def convert_file(input_path: Path, output_path: Path):
    """
    単一の .md ファイルをパースし、目次付きの .html ファイルとして出力する。
    """
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 1: Front Matter (メタデータ) と本文の分離
    metadata, body_md = parse_front_matter(content)

    title = metadata.get("title", "マイサイト")
    description = metadata.get("description", "")
    description_tag = f'  <meta name="description" content="{description}">' if description else ""

    # Step 2: 本文のHTML化 と 見出し(TOC)情報の収集
    body_html, toc_items = convert_nested_list_to_html(body_md)

    # Step 3: 収集した見出し情報から目次HTMLを生成
    toc_html = generate_toc_html(toc_items)

    # Step 4: 全体HTMLの組み立て (<body> 内の冒頭に目次を挿入)
    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
{description_tag}
</head>
<body>
<!-- ページ内目次 (TOC) -->
{toc_html}

<!-- 本文コンテンツ -->
<main>
{body_html}
</main>
</body>
</html>"""

    # Step 5: .html ファイルの保存
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"変換完了: {input_path} -> {output_path}")


def main():
    content_dir = Path("content")
    dist_dir = Path("dist")

    if not content_dir.exists():
        print("content ディレクトリが存在しません。")
        return

    for md_file in content_dir.rglob("*.md"):
        relative_path = md_file.relative_to(content_dir)
        html_file = dist_dir / relative_path.with_suffix(".html")
        convert_file(md_file, html_file)


if __name__ == "__main__":
    main()