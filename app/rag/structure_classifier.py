import re


def classify_block(text: str) -> str:
    text = text.strip()

    if not text:
        return "empty"

    # SQL / command-like content
    if text.endswith(";"):
        return "code"

    # Numbered heading:
    # 1. xxx
    # 1.1 xxx
    # 3. xxx
    if re.match(r"^\d+(\.\d+)*[\.、]\s*", text):
        return "heading"

    # Chinese numbered heading:
    # 第3章 xxx
    # 第三章 xxx
    if re.match(r"^第[一二三四五六七八九十百千万0-9]+[章节篇]\s*", text):
        return "heading"

    return "paragraph"
