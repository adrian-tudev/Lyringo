# ...existing code...
import re
from typing import Tuple
import requests

GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"


def _extract_header(formatted: str) -> Tuple[str, str]:
    if not formatted:
        return "", ""
    parts = formatted.split("\n\n", 1)
    if len(parts) == 2 and "—" in parts[0]:
        return parts[0].strip(), parts[1].strip()
    return "", formatted.strip()


def _translate_paragraph(paragraph: str, target_lang: str) -> str:
    """
    Translate a single paragraph using the unofficial Google translate web API
    (no googletrans/httpx dependency). Uses client=gtx, sl=auto.
    """
    if not paragraph.strip():
        return ""
    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": target_lang,
        "dt": "t",
        "q": paragraph
    }
    resp = requests.get(GOOGLE_TRANSLATE_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # data[0] is a list of segments: [[translated_segment, original_segment, ...], ...]
    segments = data[0]
    translated = "".join(seg[0] for seg in segments if seg and len(seg) > 0 and seg[0])
    return translated


def translate_song(lyrics: str, target_language: str) -> str:
    """
    Translate the lyrics (or formatted string) to target_language without importing
    googletrans/httpx (works on Python 3.13). Paragraphs are translated separately
    to avoid length issues.
    Returns the translated formatted string (header preserved if present).
    """
    header, body = _extract_header(lyrics)
    if not body:
        return ""

    # split into paragraphs (preserve paragraphs separated by one or more blank lines)
    paragraphs = [p for p in re.split(r'\n{2,}', body) if p.strip()]

    translated_parts = []
    for p in paragraphs:
        try:
            translated = _translate_paragraph(p, target_language)
        except Exception as e:
            # on failure, include the original paragraph so output is still usable
            translated = p
        translated_parts.append(translated)

    translated_body = "\n\n".join(translated_parts)

    if header:
        sep = "\n" + "-" * max(3, len(header)) + "\n\n"
        translated_formatted = f"{header}{sep}{translated_body}"
    else:
        translated_formatted = translated_body

    return translated_formatted
# ...existing code...