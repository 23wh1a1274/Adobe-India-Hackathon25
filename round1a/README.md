# Round 1A – PDF Outline Extractor

This tool extracts structured outlines from PDF documents using visual and typographic cues like font size, boldness, headings, and semantic patterns.

---

## 🧠 Features

- Automatically detects and ranks headings (H1, H2, H3)
- Extracts document title based on font prominence
- Heuristics for academic, technical, and multilingual PDFs
- Output is a JSON with title and outline

---

## 📦 Requirements

- Python 3.10
- PyMuPDF
- Docker (optional but recommended)

---

## 🐳 Docker Usage

1. **Build the image**:

```bash
docker build -t round1a-outline-extractor .
Prepare input and output folders:

bash
Copy
Edit
project/
├── input/
│   └── sample.pdf
├── output/
Run the container:

bash
Copy
Edit
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output round1a-outline-extractor
🧪 Output Format
Each PDF produces a JSON file like:

json
Copy
Edit
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction",
      "page": 1
    },
    ...
  ]
}
🧰 File Structure
graphql
Copy
Edit
.
├── extractor.py         # Main logic
├── requirements.txt     # Python dependencies
├── Dockerfile           # Containerization
├── input/               # PDF input folder
├── output/              # Output JSONs


👤 Tanishqa Kalidindi 
👤 Anvitha Rao
(BVRIT HYDERABAD Collage of Enigineering for Women)

Team submitted for Adobe India Hackathon Round 1A (2025)