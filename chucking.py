import re
from typing import List

def recursive_character_chunker(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    Splits text into smaller overlapping chunks based on paragraph and sentence boundaries.
    """
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        
        # If not at the end of text, try to break at a space to avoid cutting words
        if end < len(text):
            space_pos = text.rfind(' ', start, end)
            if space_pos != -1 and space_pos > start:
                end = space_pos
                
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
            
        # Move start point forward, subtracting overlap
        start = end - chunk_overlap if (end - chunk_overlap) > start else end
        
    return chunks

# --- Sample Test Document ---
sample_document = """
The James Webb Space Telescope (JWST) is a space telescope designed primarily to conduct infrared astronomy.
As the largest optical telescope in space, its high resolution and sensitivity allow it to view objects too old, distant, or faint for the Hubble Space Telescope.
JWST was launched on 25 December 2021 on an Ariane 5 rocket from Kourou, French Guiana, and arrived at the Sun–Earth L2 Lagrange point in January 2022.
The primary mirror of JWST consists of 18 hexagonal mirror segments made of gold-plated beryllium, which combined create a 6.5-meter diameter mirror.
Its primary optical observatory, the Integrated Science Instrument Module (ISIM), holds four science instruments: NIRCam, NIRSpec, NIRISS, and MIRI.
The telescope operates at temperatures below -220 °C (-364 °F) to observe faint signals in infrared without interference from its own thermal radiation.
"""

# Process document into chunks
chunks = recursive_character_chunker(sample_document, chunk_size=300, chunk_overlap=40)

print(f"Total Chunks Created: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ({len(chunk)} chars) ---")
    print(chunk)
