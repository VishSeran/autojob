import re


def normalize_text(text:str):
    return re.sub(r"[a-z0-9]", "", text.lower())
    