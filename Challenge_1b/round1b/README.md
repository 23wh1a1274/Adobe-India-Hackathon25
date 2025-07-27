📁 round1b/README.md
markdown


# 🧠 Challenge 1B — Round 1B Collections

This project processes documents for **Adobe Challenge 1B**, organized into three separate collections:

- 📂 Collection_1
- 📂 Collection_2
- 📂 Collection_3

Each collection contains its own input, output, and PDF files along with a dedicated script.

---

## 📁 Directory Structure

round1b/
│
├── Collection_1/
│ ├── PDFs/
│ ├── challenge1b_input.json
│ ├── challenge1b_output.json
│ └── run_collection.py
│
├── Collection_2/
│ ├── PDFs/
│ ├── challenge1b_input.json
│ ├── challenge1b_output.json
│ └── run_collection.py
│
├── Collection_3/
│ ├── PDFs/
│ ├── challenge1b_input.json
│ ├── challenge1b_output.json
│ └── run_collection.py
│
├── approach_explanation.md
├── requirements.txt
└── Dockerfile

---

## 🔧 Prerequisites

### 🐍 Python (Local Run)
- Python 3.8+
- All dependencies in `requirements.txt`

### 🐳 Docker (Recommended)
Ensure Docker is installed and running.

---

## 🚀 Run Instructions

### ▶️ Run Any Collection Locally (Python)

# Example: Run Collection 1
cd Collection_1
python run_collection.py
Replace Collection_1 with Collection_2 or Collection_3 as needed.

🐳 Build Docker Image (One Time)
bash


docker build -t round1b-universal .
▶️ Run Any Collection via Docker


# Run Collection 1
docker run --rm -v "${PWD}:/app" round1b-universal python Collection_1/run_collection.py

# Run Collection 2
docker run --rm -v "${PWD}:/app" round1b-universal python Collection_2/run_collection.py

# Run Collection 3
docker run --rm -v "${PWD}:/app" round1b-universal python Collection_3/run_collection.py


📦 Output
Each collection generates its own:

challenge1b_output.json file

Stored inside the respective collection folder

📘 Additional Notes
Make sure the PDFs/ folder and input JSONs are correctly populated for each collection.

All dependencies are listed in the root requirements.txt file.

📄 File: approach_explanation.md
This file outlines the logic, tools, and methodology used across all collections.