# run_collection.py (identical across collections)
import os
import json
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util

# Paths
CURRENT_DIR = Path(__file__).parent
INPUT_JSON = CURRENT_DIR / "challenge1b_input.json"
PDF_DIR = CURRENT_DIR / "PDFs"
OUTPUT_JSON = CURRENT_DIR / "challenge1b_output.json"

# Load input config
with open(INPUT_JSON) as f:
    config = json.load(f)

documents = config["documents"]
persona = config["persona"]["role"]
job = config["job_to_be_done"]["task"]

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")
query = f"{persona}: {job}"
query_embedding = model.encode(query, convert_to_tensor=True)

# Gather chunks
chunks = []
for doc in documents:
    pdf_path = PDF_DIR / doc["filename"]
    if not pdf_path.exists():
        continue
    pdf = fitz.open(pdf_path)
    for i, page in enumerate(pdf, start=1):
        text = page.get_text().strip()
        if len(text) > 100:
            chunks.append({
                "embedding": model.encode(text, convert_to_tensor=True),
                "text": text,
                "page": i,
                "document": doc["filename"],
                "title": doc["title"]
            })

# Rank chunks
scored = []
for chunk in chunks:
    score = util.cos_sim(query_embedding, chunk["embedding"]).item()
    scored.append({
        "score": score,
        "text": chunk["text"],
        "page": chunk["page"],
        "document": chunk["document"],
        "title": chunk["title"]
    })

scored.sort(key=lambda x: x["score"], reverse=True)

# Prepare output
metadata = {
    "input_documents": [doc["filename"] for doc in documents],
    "persona": persona,
    "job_to_be_done": job,
    "processing_timestamp": datetime.utcnow().isoformat()
}

extracted_sections = []
subsection_analysis = []

used_pages = set()
rank = 1
for item in scored:
    key = (item["document"], item["page"])
    if key in used_pages:
        continue
    used_pages.add(key)
    extracted_sections.append({
        "document": item["document"],
        "section_title": item["text"].split("\n")[0][:100],
        "importance_rank": rank,
        "page_number": item["page"]
    })
    subsection_analysis.append({
        "document": item["document"],
        "refined_text": item["text"][:700],
        "page_number": item["page"]
    })
    rank += 1
    if rank > 5:
        break

output = {
    "metadata": metadata,
    "extracted_sections": extracted_sections,
    "subsection_analysis": subsection_analysis
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"[✔] Processed {len(documents)} documents. Output saved to {OUTPUT_JSON.name}")
