# atai-pdf-tool

A command-line tool for parsing and extracting text from PDF files with OCR capabilities.

## Installation

```bash
pip install atai-pdf-tool
```

### Prerequisites

This tool requires Tesseract OCR to be installed on your system. Visit [Tesseract OCR Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html) for installation instructions.

## Usage

### Command Line Interface

Basic usage:

```bash
atai-pdf-tool path/to/your/document.pdf
```

With options:

```bash
atai-pdf-tool path/to/your/document.pdf -s 2 -e 5 -o output.json -l eng
```

Options:
- `-s`, `--start-page`: Starting page number (0-indexed, default: 0)
- `-e`, `--end-page`: Ending page number (0-indexed, default: last page)
- `-o`, `--output`: Output JSON file path (if not provided, prints to stdout)
- `--ocr-only`: Use OCR for all pages regardless of extractable text
- `-l`, `--lang`: Language for OCR processing (default: eng)
- `--no-progress`: Hide the progress bar (progress is shown by default)

### Supported Languages

The language option (`-l`, `--lang`) accepts language codes supported by Tesseract OCR. Some common ones include:

- `eng`: English
- `chi_sim`: Simplified Chinese
- `chi_tra`: Traditional Chinese
- `fra`: French
- `deu`: German
- `jpn`: Japanese
- `kor`: Korean
- `spa`: Spanish

For a complete list of language codes, see the [Tesseract documentation](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html).

### Language Installation

To use different languages with OCR, you need to install the corresponding language packs for Tesseract:

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr-chi-sim  # For Simplified Chinese
sudo apt-get install tesseract-ocr-fra      # For French
```

**macOS (Homebrew):**
```bash
brew install tesseract-lang  # Installs all language packs
```

**Windows:**
During Tesseract installation, select "Additional language data" and check the languages you need.

### As a Python module

```python
from atai_pdf_tool.parser import extract_pdf_pages, ocr_pdf, save_as_json

# Extract text from specific pages with English OCR
text = extract_pdf_pages("document.pdf", start_page=0, end_page=5, lang="eng")

# Extract text with different language
chinese_text = extract_pdf_pages("chinese_document.pdf", lang="chi_sim")

# Extract without progress bar
text = extract_pdf_pages("document.pdf", show_progress=False)

# Save to JSON
save_as_json(text, "output.json")

# OCR an entire PDF with a specific language
french_ocr_text = ocr_pdf("french_document.pdf", lang="fra")
```

## Features

- Extract text from PDF documents
- Automatic fallback to OCR when text extraction fails
- Support for multiple languages via Tesseract OCR
- Progress bar for tracking processing of large documents
- Clean and normalize extracted text
- Save results in JSON format or print to stdout
- Specify page ranges for extraction

## License

This project is licensed under the MIT License - see the LICENSE file for details.