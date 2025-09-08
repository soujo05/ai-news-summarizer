# text_cleaning.py
import html
import re
import unicodedata
try:
    from ftfy import fix_text as _ftfy_fix
except Exception:
    _ftfy_fix = None

_ZW = ["\u200b", "\u200c", "\u200d", "\ufeff"]

def fix_mojibake(s: str) -> str:
    """Fix UTF-8/Windows-1252 mojibake, HTML entities, and normalize."""
    if not s:
        return ""
    # Convert &rsquo; etc.
    s = html.unescape(s)
    # Repair mojibake like "Trumpâ€™s"
    if _ftfy_fix:
        s = _ftfy_fix(s)
    # Normalize and strip zero-width/control chars
    s = unicodedata.normalize("NFC", s)
    for z in _ZW:
        s = s.replace(z, "")
    s = re.sub(r"[\u0000-\u001f\u007f]", "", s)
    return s
