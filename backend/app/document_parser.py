import io
import re
from typing import Tuple, Dict, Any, Optional

class DocumentParser:
    """
    Multi-Format Document Extraction & Untrusted Ingestion Sanitizer (Section IV.E)
    Supports PDF, DOCX, TXT, MD, CSV, and sanitizes indirect prompt injections.
    """
    def __init__(self):
        self.injection_markers = [
            r"\[\s*system\s*instruction.*?\b\]",
            r"<\s*system.*?>.*?</\s*system\s*>",
            r"ignore\s+(all\s+)?previous\s+instructions",
            r"you\s+must\s+now\s+act\s+as",
            r"exfiltrate\s+all",
            r"reveal\s+confidential\s+records"
        ]

    def parse_file(self, file_bytes: bytes, file_name: str, content_type: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        name_lower = file_name.lower()
        metadata = {
            "file_name": file_name,
            "format": "text",
            "sanitized": False,
            "threats_neutralized": 0
        }
        raw_text = ""

        # PDF parsing
        if name_lower.endswith(".pdf") or (content_type and "pdf" in content_type):
            metadata["format"] = "pdf"
            try:
                import pypdf
                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                pages = [page.extract_text() or "" for page in reader.pages]
                raw_text = "\n\n".join(pages)
            except Exception as e:
                # Fallback to string extraction if library not loaded
                raw_text = file_bytes.decode("utf-8", errors="ignore")

        # DOCX parsing
        elif name_lower.endswith(".docx") or (content_type and "wordprocessingml" in content_type):
            metadata["format"] = "docx"
            try:
                import docx
                doc = docx.Document(io.BytesIO(file_bytes))
                paragraphs = [p.text for p in doc.paragraphs if p.text]
                raw_text = "\n\n".join(paragraphs)
            except Exception:
                raw_text = file_bytes.decode("utf-8", errors="ignore")

        # Plain Text / Markdown / CSV
        else:
            try:
                raw_text = file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                raw_text = file_bytes.decode("latin-1", errors="ignore")

        # Untrusted Content Inspection (Flow 6 & 9 on Ingestion)
        sanitized_text, threats_count = self.sanitize_untrusted_text(raw_text)
        metadata["sanitized"] = threats_count > 0
        metadata["threats_neutralized"] = threats_count

        return sanitized_text, metadata

    def sanitize_untrusted_text(self, text: str) -> Tuple[str, int]:
        """Strip embedded indirect prompt injections from ingested documents"""
        threats_count = 0
        cleaned = text

        for pattern in self.injection_markers:
            matches = re.findall(pattern, cleaned, flags=re.IGNORECASE | re.DOTALL)
            if matches:
                threats_count += len(matches)
                cleaned = re.sub(pattern, "[DEFANGED_PROMPT_INJECTION_REMOVED]", cleaned, flags=re.IGNORECASE | re.DOTALL)

        return cleaned, threats_count

document_parser = DocumentParser()
