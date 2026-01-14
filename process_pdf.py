import json, os, uuid, re
from pypdf import PdfReader
import nltk
import pytesseract
from PIL import Image
import io

nltk.download("punkt", quiet=True)

def clean_text(text: str) -> str:
    """Normalize whitespace and remove common header/footer boilerplate and ligatures."""
    text = re.sub(r'HCLTech\s+Annual\s+Integrated\s+Report\s+2024–25', '', text)
    text = re.sub(r'Annual\s+Report\s+2024-25', '', text)
    text = re.sub(r'P\s?a\s?g\s?e\s+\d+', '', text)
    
    # Fix common PDF extraction artifacts / ligatures
    text = text.replace("/r_t.liga", "rt").replace("/r_f.liga", "rf")
    text = text.replace("t_t.liga", "tt").replace("f_f.liga", "ff")
    text = text.replace("/uni20B9", "₹") # Fix currency symbol
    
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text, max_words=300, overlap_words=60):
    """Segment text into sentence-aware chunks with overlap for better context."""
    sentences = nltk.sent_tokenize(text)
    chunks, current_chunk, current_len = [], [], 0

    for sent in sentences:
        words = sent.split()
        if current_len + len(words) > max_words:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            # Maintain overlap
            overlap = current_chunk[-overlap_words:] if overlap_words < len(current_chunk) else current_chunk
            current_chunk = overlap + words
            current_len = len(current_chunk)
        else:
            current_chunk.extend(words)
            current_len += len(words)

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    # Filter out very small chunks that likely lack context
    return [c for c in chunks if len(c.split()) > 40]

def detect_section(text: str) -> str:
    """Detect section headings based on uppercase text and keywords."""
    lines = text.split("\n")
    # Check first 5 lines for a clear title
    for line in lines[:5]:
        line = line.strip()
        if line.isupper() and 2 < len(line.split()) < 12:
            return line
            
    # Secondary keyword check if no clear title found
    text_lower = text.lower()
    if "financial highlights" in text_lower or "consolidated financial" in text_lower:
        return "Financial Statements"
    if "human resource" in text_lower or "people and culture" in text_lower or "employees" in text_lower:
        return "Human Resources"
    if "governance" in text_lower or "board of directors" in text_lower:
        return "Governance"
    if "risk management" in text_lower:
        return "Risk Management"
    if "environmental" in text_lower or "sustainability" in text_lower or "esg" in text_lower:
        return "Sustainability"

    return "N/A"

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_page_images(page):
    """Extract text from images in PDF using OCR."""
    text = ""
    try:
        if page.images:
            for image_file_object in page.images:
                image_data = image_file_object.data
                image = Image.open(io.BytesIO(image_data))
                text += pytesseract.image_to_string(image) + "\n"
    except Exception as e:
        print(f"Warning: OCR failed. Error: {e}")
    return text

def process_pdf(pdf_path, output_path):
    print(f"Processing {pdf_path}...")
    reader = PdfReader(pdf_path)
    all_chunks = []
    doc_title = "HCLTech Annual Integrated Report 2024–25"
    version = "latest"

    total_pages = len(reader.pages)
    for i, page in enumerate(reader.pages):
        page_number = i + 1
        if page_number % 25 == 0:
            print(f"Page {page_number}/{total_pages}...")

        text = page.extract_text()
        
        if not text or len(text.strip()) < 50:
            ocr_text = ocr_page_images(page)
            if ocr_text.strip():
                text = ocr_text if not text else text + "\n" + ocr_text

        if not text:
            continue

        section = detect_section(text) 
        cleaned_text = clean_text(text)
        page_chunks = chunk_text(cleaned_text)

        for chunk_content in page_chunks:
            all_chunks.append({
                "doc_title": doc_title,
                "page_number": page_number,
                "section": section,
                "chunk_id": str(uuid.uuid4()),
                "version": version,
                "content": chunk_content,
                "word_count": len(chunk_content.split())
            })

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, indent=2)
    print(f"Done. Total chunks: {len(all_chunks)}")

if __name__ == "__main__":
    pdf_file = "Annual-Report-2024-25.pdf"
    output_file = "chunks.json"
    if os.path.exists(pdf_file):
        process_pdf(pdf_file, output_file)
    else:
        print(f"Error: {pdf_file} not found.")

