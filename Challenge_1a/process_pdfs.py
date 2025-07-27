import fitz  # PyMuPDF
import os
import json
from collections import Counter
from pathlib import Path
import re

# Updated input/output paths
INPUT_DIR = Path("/app/sample_dataset/pdfs")
OUTPUT_DIR = Path("/app/sample_dataset/outputs")

HEADING_KEYWORDS = [
    'introduction', 'overview', 'background', 'methodology', 'results',
    'conclusion', 'abstract', 'summary', 'discussion', 'analysis',
    'chapter', 'section', 'part', 'appendix', 'references', 'bibliography',
    'contents', 'index', 'preface', 'acknowledgments', 'table of contents',
    'はじめに', '概要', '結論', '参考文献', '目次', '付録'
]

def clean_text(text):
    return " ".join(text.strip().split())

def is_meaningful(text):
    return len(text.strip()) > 0 and not text.strip().isdigit()

def classify_heading(line_text, avg_size, font_names, body_size, heading_sizes):
    is_caps = line_text.isupper()
    is_short = len(line_text.split()) <= 12
    is_bold = any("bold" in fn.lower() or "bd" in fn.lower() for fn in font_names)
    has_keyword = any(kw in line_text.lower() for kw in HEADING_KEYWORDS)

    if avg_size >= heading_sizes[0] or (is_bold and is_caps and avg_size >= body_size):
        return "H1"
    elif avg_size >= heading_sizes[1] or (is_bold and (is_caps or has_keyword) and avg_size >= body_size):
        return "H2"
    elif avg_size > body_size or has_keyword:
        return "H3"
    return None

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    font_sizes = []

    # Pass 1: Collect font sizes
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    font_sizes.append(round(span["size"]))

    size_counts = Counter(font_sizes)
    most_common_sizes = [s for s, _ in size_counts.most_common()]
    body_size = most_common_sizes[-1] if len(most_common_sizes) > 1 else most_common_sizes[0]
    heading_sizes = sorted(set(s for s in font_sizes if s > body_size), reverse=True)[:2]
    if len(heading_sizes) < 2:
        heading_sizes = [body_size + 2, body_size + 1]

    headings = []
    max_font_size = 0
    title_text = ""

    # Pass 2: Extract headings
    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                line_text = ""
                font_sizes_line = []
                font_names = set()

                for span in line.get("spans", []):
                    text = clean_text(span["text"])
                    if not text:
                        continue
                    line_text += text + " "
                    font_sizes_line.append(round(span["size"]))
                    font_names.add(span.get("font", ""))

                line_text = clean_text(line_text)
                if not is_meaningful(line_text):
                    continue

                avg_size = sum(font_sizes_line) / len(font_sizes_line) if font_sizes_line else 0
                if avg_size > max_font_size:
                    max_font_size = avg_size
                    title_text = line_text

                level = classify_heading(line_text, avg_size, font_names, body_size, heading_sizes)
                if level:
                    headings.append({
                        "level": level,
                        "text": line_text,
                        "page": page_number
                    })

    return {
        "title": title_text,
        "outline": headings
    }

def main():
    print("📥 Starting processing PDFs...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_files = list(INPUT_DIR.glob("*.pdf"))

    if not pdf_files:
        print("❗ No PDF files found in input directory.")
        return

    for pdf_file in pdf_files:
        print(f"🔍 Processing: {pdf_file.name}")
        outline = extract_outline_from_pdf(pdf_file)
        output_file = OUTPUT_DIR / f"{pdf_file.stem}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(outline, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved: {output_file.name}")

    print("🎉 Completed processing all PDFs.")

if __name__ == "__main__":
    main()
