def is_empty(text: str) -> bool:
    return not text or text.strip() == ""

def sanitize_input(text: str) -> str:
    return text.strip()[:1000]  # ограничение длины