import os
from os.path import join
import markdown  # ✅ 用于渲染 Markdown -> HTML

def load_template(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as handle:
        return handle.read()

MAX_LINKS = 90

if __name__ == '__main__':
    template = load_template('template.md')
    index_template = load_template('index_template.md')
    readme_content_template = load_template('readme_content_template.md')

    entries = sorted(os.listdir('data'), reverse=True)
    md_entries = [item for item in entries if item.endswith('.md')][:MAX_LINKS]

    line_template = readme_content_template.strip()

    readme_lines = [
        line_template.format(
            date=item.replace('.md', ''),
            url=join('data', item.replace('.md', '.html'))
        )
        for item in md_entries
    ]
    readme_content = "\n".join(readme_lines) if readme_lines else '_(no digests yet)_'

    markdown_text = template.format(readme_content=readme_content)
    with open('README.md', 'w', encoding='utf-8') as handle:
        handle.write(markdown_text)

    if md_entries:
        latest_md = md_entries[0]
        latest_date = latest_md.replace('.md', '')
        latest_path = join('data', latest_md.replace('.md', '.html'))
    else:
        latest_date = 'No reports yet'
        latest_path = '#'

    history_lines = readme_lines
    history = "\n".join(history_lines) if history_lines else '_(empty)_'

    index_markdown = index_template.format(
        latest_date=latest_date,
        latest_path=latest_path,
        history=history
    )
    with open('index.md', 'w', encoding='utf-8') as handle:
        handle.write(index_markdown)

    # ======================================================
    # ✅ Markdown -> HTML 渲染（GitHub Pages 可直接展示）
    # ======================================================
    try:
        html_body = markdown.markdown(
            index_markdown,
            extensions=[
                "extra",        # 支持表格、脚注、缩进列表
                "codehilite",   # 支持代码高亮
                "fenced_code",  # 支持 ``` 代码块
                "tables",       # 支持表格语法
                "toc"           # 自动生成目录
            ]
        )

        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Daily arXiv Digest</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    <style>
        body {{
            background-color: #fafafa;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            padding: 2rem;
        }}
        .markdown-body {{
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        pre code {{
            background-color: #f6f8fa;
            padding: 0.5em;
            border-radius: 6px;
        }}
    </style>
</head>
<body>
    <article class="markdown-body">
        {html_body}
    </article>
</body>
</html>"""

        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_template)
        print("✅ Successfully generated index.html with Markdown rendering.")
    except Exception as e:
        print(f"⚠️ Failed to generate index.html: {e}")
