import re


def markdown_to_blocks(markdown):
    lines = list(filter(lambda x: x != "", map(str.strip, re.split(r'\r?\n\r?\n', markdown))))
    print(lines)
    return lines


def extract_title(markdown:str):
    lines = markdown.splitlines()
    for line in lines:
        if line.strip().startswith("# "):
            return line.lstrip("# ")
    raise Exception("No header")

