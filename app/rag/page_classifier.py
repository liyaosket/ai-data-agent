def is_table_of_contents(page_text: str) -> bool:
    text = page_text.strip()

    if not text:
        return False

    return "目录" in text
