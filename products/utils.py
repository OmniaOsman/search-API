import re
import unicodedata

# Remove Arabic diacritics
ARABIC_DIACRITICS = re.compile(r"[\u0617-\u061A\u064B-\u0652]")

def normalize_text(text):
    if not text:
        return ''
    # Remove diacritics
    text = ARABIC_DIACRITICS.sub('', text)
    # Normalize unicode
    text = unicodedata.normalize('NFKC', text)
    # Convert Arabic/English numbers to English
    text = text.translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789'))
    # Lowercase
    text = text.lower()
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text
