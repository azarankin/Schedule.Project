# utils_rtl.py
import locale
import os

def setup_hebrew_locale():
    os.environ["LANG"] = "he_IL.utf8"
    for loc in ['he_IL.utf8', 'en_US.utf8', 'C']:
        try:
            locale.setlocale(locale.LC_TIME, loc)
            break
        except locale.Error:
            continue

def is_hebrew(text):
    return any('\u0590' <= ch <= '\u05EA' for ch in text)

def reverse_if_hebrew(word):
    return word[::-1] if is_hebrew(word) else word

def reorder_mixed_rtl(text):
    return ' '.join(w[::-1] if is_hebrew(w) else w for w in text.split())
