import io
import re
from typing import Tuple
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document

def _safe_text(s: str) -> str:
    s = s.replace("\x00", " ")
    return re.sub(r"[ \t]+", " ", s).strip()

def _parse_pdf(blob: bytes) -> str:
    with io.BytesIO(blob) as fh:
        txt = pdf_extract_text(fh) or ""
    return _safe_text(txt)

def _parse_docx(blob: bytes) -> str:
    with io.BytesIO(blob) as fh:
        doc = Document(fh)
    txt = "\n".join(p.text for p in doc.paragraphs)
    return _safe_text(txt)

def _parse_txt(blob: bytes) -> str:
    try:
        return _safe_text(blob.decode("utf-8", errors="ignore"))
    except Exception:
        return _safe_text(blob.decode("latin-1", errors="ignore"))

def parse_resume(filename: str, blob: bytes) -> Tuple[str, str]:
    name_guess = filename.rsplit(".", 1)[0]
    name_guess = re.sub(r"[_\-]+", " ", name_guess).title()

    if filename.lower().endswith(".pdf"):
        text = _parse_pdf(blob)
    elif filename.lower().endswith(".docx"):
        text = _parse_docx(blob)
    else:
        text = _parse_txt(blob)

    # crude name heuristic from resume header
    line1 = (text.splitlines() or [""])[0]
    maybe_name = re.sub(r"[^A-Za-z .'-]", "", line1).strip()
    if 3 <= len(maybe_name) <= 60 and "@" not in maybe_name:
        name_guess = maybe_name

    return text, name_guess or "Candidate"
