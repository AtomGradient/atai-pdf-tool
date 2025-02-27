from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="atai-pdf-tool",
    version="0.0.3",
    author="AtomGradient",
    author_email="alex@atomgradient.com",
    description="A tool for parsing and extracting text from PDF files with OCR capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AtomGradient/atai-pdf-tool",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyPDF2",
        "PyMuPDF",
        "pytesseract",
        "Pillow",
        "PyCryptodome"
    ],
    entry_points={
        "console_scripts": [
            "atai-pdf-tool=atai_pdf_tool.cli:main",
        ],
    },
)