import re
from pathlib import Path

def clean_mdx(file_path):
    text = Path(file_path).read_text()

    # remove JSX tags
    text = re.sub(r"<.*?>", "", text)

    # remove import lines
    text = re.sub(r"import .*", "", text)

    return text


src = Path("/Users/kishansevanan/Documents/Project/docs_rag/data/raw_docs/langgraph")

for mdx_file in src.rglob("*.mdx"):
    cleaned = clean_mdx(mdx_file)

    new_file = mdx_file.with_suffix(".md")
    new_file.write_text(cleaned)

print("Converted MDX → MD")