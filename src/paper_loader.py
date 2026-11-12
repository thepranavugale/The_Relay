
import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader
from config import PAPERS_DIR, PROCESSED_DIR


# --------------------------------------------------
# 1. RESEARCH PAPER DETAILS
# --------------------------------------------------

PAPER_FILES = {
    "Attention Is All You Need":
        "attention_is_all_you_need_v7.pdf",

    "Moshi: A Speech-Text Foundation Model":
        "moshi_v1.pdf",

    "Dynamic Chunking for End-to-End Hierarchical Sequence Modeling":
        "dynamic_chunking_v2.pdf"
}


# --------------------------------------------------
# 2. TEXT CLEANING
# --------------------------------------------------

def clean_text(text):
    """Remove unnecessary whitespace from extracted text."""

    if not text:
        return ""

    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# --------------------------------------------------
# 3. TEXT CHUNKING
# --------------------------------------------------

def create_chunks(text, chunk_size=1000, overlap=150):
    """
    Divide text into smaller overlapping chunks.

    chunk_size: Maximum approximate characters per chunk.
    overlap: Characters repeated between consecutive chunks.
    """

    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")

    text = clean_text(text)

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):

        end = min(start + chunk_size, len(text))

        # Try to end at a word boundary
        if end < len(text):
            space_position = text.rfind(" ", start, end)

            if space_position > start:
                end = space_position

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        next_start = end - overlap

        # Ensure forward progress
        start = max(start + 1, next_start)

    return chunks


# --------------------------------------------------
# 4. EXTRACT TEXT FROM PDF
# --------------------------------------------------

def extract_pdf_text(pdf_path):

    print(f"\nReading PDF: {pdf_path.name}")

    reader = PdfReader(str(pdf_path), strict=False)

    if reader.is_encrypted:
        raise ValueError(
            f"PDF is encrypted: {pdf_path.name}"
        )

    page_data = []

    for page_number, page in enumerate(reader.pages, start=1):

        extracted_text = page.extract_text() or ""

        cleaned_text = clean_text(extracted_text)

        if cleaned_text:

            page_data.append({
                "page": page_number,
                "text": cleaned_text
            })

    return page_data


# --------------------------------------------------
# 5. BUILD PAPER CHUNKS
# --------------------------------------------------

def process_paper(title, filename):

    pdf_path = PAPERS_DIR / filename

    if not pdf_path.exists():

        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    pages = extract_pdf_text(pdf_path)

    paper_chunks = []

    for page in pages:

        chunks = create_chunks(
            page["text"],
            chunk_size=1000,
            overlap=150
        )

        for chunk_number, chunk in enumerate(chunks, start=1):

            record = {
                "paper": title,
                "file": filename,
                "page": page["page"],
                "chunk": chunk_number,
                "text": chunk
            }

            paper_chunks.append(record)

    print(f"Pages processed: {len(pages)}")
    print(f"Chunks created: {len(paper_chunks)}")

    return paper_chunks


# --------------------------------------------------
# 6. SAVE CHUNKS INTO JSONL FILE
# --------------------------------------------------

def save_chunks(all_chunks):

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = PROCESSED_DIR / "chunks.jsonl"

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        for record in all_chunks:

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )

    print("\n--------------------------------")
    print("CHUNK SAVING COMPLETED")
    print("--------------------------------")

    print(f"Total chunks: {len(all_chunks)}")
    print(f"Output file: {output_path}")


# --------------------------------------------------
# 7. MAIN FUNCTION
# --------------------------------------------------

def build_index():

    print("================================")
    print("THE RELAY - PAPER LOADER")
    print("================================")

    all_chunks = []

    for title, filename in PAPER_FILES.items():

        print(f"\nProcessing: {title}")

        paper_chunks = process_paper(
            title,
            filename
        )

        all_chunks.extend(paper_chunks)

    if not all_chunks:
        raise RuntimeError(
            "No text extracted. Check your PDF files."
        )

    save_chunks(all_chunks)

    print("\nPaper loading completed successfully!")


# --------------------------------------------------
# 8. PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    try:
        build_index()

    except Exception as error:

        print("\nERROR:", error)
        sys.exit(1)
