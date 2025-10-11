import json
import argparse
import os
from itertools import count
import markdown  # ✅ 新增：用于 Markdown -> HTML 渲染

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="Path to the jsonline file")
    args = parser.parse_args()
    data = []
    preference = os.environ.get('CATEGORIES', 'cs.CV, cs.CL').split(',')
    preference = list(map(lambda x: x.strip(), preference))
    def rank(cate):
        if cate in preference:
            return preference.index(cate)
        else:
            return len(preference)

    with open(args.data, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))

    categories = set([item["categories"][0] for item in data])
    template = open("paper_template.md", "r", encoding="utf-8").read()
    categories = sorted(categories, key=rank)
    cnt = {cate: 0 for cate in categories}
    for item in data:
        if item["categories"][0] not in cnt.keys():
            continue
        cnt[item["categories"][0]] += 1

    # ========== 生成 Markdown 文本 ==========
    markdown_text = f"<div id=toc></div>\n\n# Table of Contents\n\n"
    for idx, cate in enumerate(categories):
        markdown_text += f"- [{cate}](#{cate}) [Total: {cnt[cate]}]\n"

    idx = count(1)
    for cate in categories:
        markdown_text += f"\n\n<div id='{cate}'></div>\n\n"
        markdown_text += f"# {cate} [[Back]](#toc)\n\n"
        markdown_text += "\n\n".join(
            [
                template.format(
                    title=item["title"],
                    authors=", ".join(item["authors"]),
                    summary=item["summary"],
                    url=item['abs'],
                    tldr=item['AI']['tldr'],
                    motivation=item['AI']['motivation'],
                    method=item['AI']['method'],
                    result=item['AI']['result'],
                    conclusion=item['AI']['conclusion'],
                    cate=item['categories'][0],
                    idx=next(idx)
                )
                for item in data if item["categories"][0] == cate
            ]
        )

    # ========== 保存 Markdown ==========
    output_md = args.data.split('_')[0] + '.md'
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    print(f"✅ Markdown saved to {output_md}")

    # ========== 转换为 HTML ==========
    html_body = markdown.markdown(
        markdown_text,
        extensions=["extra", "codehilite", "fenced_code", "tables", "toc"]
    )

    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{os.path.basename(output_md)}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script>hljs.highlightAll();</script>
  <style>
    body {{
      background-color: #fafafa;
      font-family: 'Inter', sans-serif;
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
  </style>
</head>
<body>
  <article class="markdown-body">
    {html_body}
  </article>
</body>
</html>
"""

    output_html = output_md.replace(".md", ".html")
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"✅ HTML saved to {output_html}")
