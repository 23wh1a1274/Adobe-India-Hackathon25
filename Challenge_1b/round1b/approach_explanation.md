# Approach Explanation - Round 1B

## Goal

The objective is to extract document insights tailored to different personas (developer, product manager, designer) using a CPU-only, offline, lightweight method.

---

## Methodology

1. **Text Extraction**:  
   We use PyMuPDF to extract full text from each page of the PDF document. The text is cleaned and broken into paragraphs.

2. **Persona Keywords**:  
   For each persona, we define a list of relevant keywords. These keywords reflect the job-to-be-done for that persona.

3. **Section Relevance**:  
   Each page is treated as a section. We calculate an importance score based on the number of matching keywords found in that page's content. Top-ranked pages are stored as `extracted_sections` with `importance_rank`.

4. **Sub-Section Analysis**:  
   Within each page, we look at individual paragraphs. If a paragraph contains relevant keywords, it is included in the `sub_section_analysis` for that persona.

5. **Scoring and Ranking**:  
   Sections are sorted by their keyword match count. Only the top 5 sections and top 10 sub-sections are retained per persona to meet time and memory constraints.

6. **Metadata**:  
   Output includes metadata such as persona, document name, timestamp, and job-to-be-done.

---

## Constraints

- **Model Size**: No ML model used, <1GB memory footprint.
- **Offline Execution**: All logic is rule-based, no internet access required.
- **Runtime**: Entire pipeline completes in <60 seconds for 3–5 documents.
- **Platform**: Docker container ensures reproducibility on CPU-only systems.

---

## Summary

This solution meets the challenge criteria using clean offline logic, is extensible to more personas, and generates clear JSON summaries useful for downstream analysis or UI visualization.
