# 🧠 Challenge 1A — PDF Outline Extraction

This project extracts structured outlines (titles and headings) from academic or technical PDFs using font size, style, and keyword heuristics. The outputs are saved as JSON files for each PDF.

---

## 📁 Project Structure

Challenge_1a/
├── process_pdfs.py # Main script for PDF outline extraction
├── requirements.txt # Dependencies
├── Dockerfile # Docker container specification
└── sample_dataset/
├── pdfs/ # Place input PDFs here
└── outputs/ # Extracted JSON output files appear here



---

## ⚙️ Requirements

- Python 3.8+ (if running locally)
- Docker (recommended for environment consistency)

---

## 🐍 Local Setup (Optional)

### 1. Create virtual environment and activate:


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
2. Install dependencies
bash:
pip install -r requirements.txt
3. Run the script
bash:
python process_pdfs.py
Make sure your PDFs are in sample_dataset/pdfs. The outputs will be saved in sample_dataset/outputs.

🐳 Docker Setup (Recommended)
1. Build Docker Image
From the root of Challenge_1a:

powershell:

docker build -t process-pdfs-round1a .
2. Run Container (PowerShell on Windows)
powershell:

docker run --rm `
  -v "${PWD}\sample_dataset\pdfs:/app/sample_dataset/pdfs" `
  -v "${PWD}\sample_dataset\outputs:/app/sample_dataset/outputs" `
  process-pdfs-round1a
Alternatively (single line):

powershell:

docker run --rm -v "${PWD}\sample_dataset\pdfs:/app/sample_dataset/pdfs" -v "${PWD}\sample_dataset\outputs:/app/sample_dataset/outputs" process-pdfs-round1a

📦 Output
For each PDF in sample_dataset/pdfs/, a corresponding .json file will be created in sample_dataset/outputs/.

Each output file contains:

Title of the document (based on font size)

Outline of headings with levels (H1, H2, H3) and page numbers

🛠️ Notes
The logic supports multilingual PDFs and detects headings using:

Font size ranking

Capitalization

Font weight (bold)

Heading-related keywords (e.g., "Abstract", "Methodology", etc.)

📄 Sample Output

{
  "title": "A Survey on AI Techniques",
  "outline": [
    {"level": "H1", "text": "Introduction", "page": 1},
    {"level": "H2", "text": "Deep Learning", "page": 3},
    {"level": "H3", "text": "Convolutional Networks", "page": 4}
  ]
}
👤 Author
TEAM:Tanishqa 
Tanishqa Kalidindi ,Anvitha Rao
| Adobe Challenge Submission – Round 1A