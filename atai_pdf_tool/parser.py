import re
import json
import io
from typing import Optional, Dict, Any

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader


def extract_text_with_ocr(pdf_path: str, page_num: int, lang: str = "eng") -> str:
    """Extract text from a PDF page using OCR."""
    # Read page as image
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    pix = page.get_pixmap()
    img_bytes = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_bytes))
    # Extract text using OCR
    text = pytesseract.image_to_string(img, lang=lang)
    return text


def is_valid_text(text: str) -> bool:
    """Check if extracted text is valid."""
    # Basic cleaning, remove excessive whitespace
    cleaned_text = re.sub(r'[\t\r\n]+', ' ', text).strip()
    # Check if text contains enough English word characters and numbers
    if re.search(r'[A-Za-z0-9]{3,}', cleaned_text):
        return True
    # Check if text contains meaningful sentences
    if re.search(r'([A-Za-z]+ ){2,}', cleaned_text):
        return True
    return False


def extract_pdf_pages(pdf_path: str, start_page: int = 0, end_page: Optional[int] = None, lang: str = "eng") -> str:
    """Extract text from PDF pages, using OCR if necessary."""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        if start_page < 0 or start_page >= total_pages:
            print(f"Invalid start page number. Using 0 instead of {start_page}.")
            start_page = 0
            
        if end_page is None:
            end_page = total_pages - 1
        elif end_page < start_page or end_page >= total_pages:
            print(f"Invalid end page number. Using {total_pages - 1} instead of {end_page}.")
            end_page = total_pages - 1
            
        text = ''
        for page_num in range(start_page, end_page + 1):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            if page_text and is_valid_text(page_text):
                text += page_text
            else:
                # If text extraction fails, use OCR
                text += extract_text_with_ocr(pdf_path, page_num, lang=lang)
        return text


def clean_text(text: str) -> str:
    """Clean and escape text for JSON formatting."""
    # Remove non-ASCII characters
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
    cleaned_text = cleaned_text.replace('\n', '')
    cleaned_text = cleaned_text.replace('"', "'")
    # Clean control characters
    cleaned_string = clean_control_characters(cleaned_text)
    cleaned_string = cleaned_string.replace("\\", "\\\\")
    cleaned_string = cleaned_string.replace("\"", "\\\"")
    return cleaned_string


def clean_control_characters(s: str) -> str:
    """Clean control characters from a string."""
    cleaned = ""
    for char in s:
        # Handle ASCII control characters
        if ord(char) < 32:
            # Allow newlines, carriage returns, and tabs, but escape them
            if char in '\n\r\t':
                cleaned += char.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
        else:
            # Add other characters directly
            cleaned += char
    return cleaned


def save_as_json(text: str, output_file: str) -> None:
    """Save extracted text as JSON."""
    cleaned_text = clean_text(text)
    data = {"text": cleaned_text}
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def ocr_pdf(pdf_path: str, lang: str = "eng") -> str:
    """Extract text from an entire PDF using OCR."""
    doc = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(len(doc)):
        # Get page
        page = doc.load_page(page_num)
        
        # Get image from page
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        
        # Extract text using OCR
        page_text = pytesseract.image_to_string(img, lang=lang)
        text += page_text
    
    return text