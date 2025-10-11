import os
from os.path import join


def load_template(path: str) -> str:
    with open(path, 'r') as handle:
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
            url=join('data', item)
        )
        for item in md_entries
    ]
    readme_content = "\n".join(readme_lines) if readme_lines else '_(no digests yet)_'

    markdown = template.format(readme_content=readme_content)
    with open('README.md', 'w') as handle:
        handle.write(markdown)

    if md_entries:
        latest_md = md_entries[0]
        latest_date = latest_md.replace('.md', '')
        latest_path = join('data', latest_md)
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
    with open('index.md', 'w') as handle:
        handle.write(index_markdown)
