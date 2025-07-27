# multi_collection.py

import os
import json
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util

def process_collection(collection_path: Path, model):
    print(f"\n📂 Processing {collection_path.name}")

    input_json = collection_path / "challenge1b_input.json"
    pdf_dir = collection_path / "PDFs"
    output_json = collection_path / "challenge1b_output.json"

    if not input_json.exists() or not pdf_dir.exists():
        print(f"⚠️ Missing input JSON or PDFs folder in {collection_path.name}")
        return

    with open(input_json) as f:
        config = json.load(f)

    documents = config.get("documents", [])
    persona = config.get("persona", {}).get("role", "")
    job = config.get("job_to_be_done", {}).get("task", "")

    query = f"{persona}: {job}"
    query_embedding = model.encode(query, convert_to_tensor=True)

    chunks = []
    for doc in documents:
        pdf_path = pdf_dir / doc["filename"]
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
                    "title": doc.get("title", "")
                })

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

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Output saved to {output_json.name}")


def main():
    base_dir = Path(__file__).parent
    collections = ["Collection 1", "Collection 2", "Collection 3"]

    print("🔍 Loading model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    for collection in collections:
        collection_path = base_dir / collection
        if collection_path.exists():
            process_collection(collection_path, model)
        else:
            print(f"⚠️ Collection folder not found: {collection}")


if __name__ == "__main__":
    main()
