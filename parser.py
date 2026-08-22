import io
import re
from typing import List, Dict, Any
from pypdf import PdfReader

def parse_pdf_bytes(pdf_bytes: bytes, filename: str) -> List[Dict[str, Any]]:
    """
    Parses PDF bytes and extracts text page by page with metadata.
    """
    reader = PdfReader(io.BytesIO(pdf_bytes))
    documents = []
    
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = re.sub(r'\s+', ' ', text).strip()
        if text:
            documents.append({
                "text": text,
                "metadata": {
                    "source": filename,
                    "page": page_num
                }
            })
            
    return documents

def metadata_aware_chunker(documents: List[Dict[str, Any]], chunk_size: int = 400, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Chunks pages while preserving page numbers and source metadata.
    """
    chunks = []
    chunk_counter = 0
    
    for doc in documents:
        text = doc["text"]
        start = 0
        while start < len(text):
            end = start + chunk_size
            if end < len(text):
                space_pos = text.rfind(' ', start, end)
                if space_pos > start:
                    end = space_pos
                    
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    "id": f"chunk_{chunk_counter}",
                    "text": chunk_text,
                    "metadata": {
                        "source": doc["metadata"]["source"],
                        "page": doc["metadata"]["page"],
                        "chunk_id": chunk_counter
                    }
                })
                chunk_counter += 1
                
            start = end - chunk_overlap if (end - chunk_overlap) > start else end
            
    return chunks

# --- Create Sample Documents for Demonstration ---
doc_a = """
The James Webb Space Telescope (JWST) operating manual.
Section 1.1: Thermal Controls.
JWST uses a 5-layer Kapton sunshield to maintain operating temperatures below -220°C.
Part ID for Sunshield Replacement: KAP-9082-JWST.
"""

doc_b = """
Hubble Space Telescope (HST) vs JWST Comparison Report.
HST orbits Earth at ~547 km altitude, while JWST orbits the Sun-Earth L2 point at ~1.5 million km.
HST primarily observes ultraviolet and visible light, whereas JWST focuses on infrared.
Part ID for Hubble Mirror Assembly: HUB-1002-HST.
"""

# Simulate loading multiple documents
raw_docs = [
    {"text": doc_a, "metadata": {"source": "JWST_Manual.pdf", "page": 1}},
    {"text": doc_b, "metadata": {"source": "Hubble_vs_JWST.pdf", "page": 1}},
]

processed_chunks = metadata_aware_chunker(raw_docs, chunk_size=200, chunk_overlap=30)
print(f"Total Chunks Created across documents: {len(processed_chunks)}")
print("Sample Chunk Metadata:", processed_chunks[0]["metadata"])
