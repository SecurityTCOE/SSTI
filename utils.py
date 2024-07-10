# utils.py

import re

def custom_tokenizer(text):
    tokens = re.findall(r'\b\w+\b|\S', text)
    return tokens
