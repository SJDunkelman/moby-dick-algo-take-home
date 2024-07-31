import re


def preprocess_text_to_list(text: str) -> list[str]:
    text = re.sub(r'[ .,();{}\[\]]', "\n", text)
    words = text.split('\n')
    # Remove empty strings, equivalent to grep -v "^$"
    return [word for word in words if word]