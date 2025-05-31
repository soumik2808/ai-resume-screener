# 🤖 AI Resume Tool

A modular Flask-based web app to assist in all things related to resumes — from smart screening with job descriptions to generating structured resumes via a form.

---

## 🔍 Features

### Resume Screener
- Upload Resume and Job Description (PDF or DOCX)
- Extracts and compares key skills using `KeyBERT`
- Displays:
  - Resume Match Score (out of 100)
  - Matched vs Missing Skills
  - Full Text Extraction (both resume and JD)

### Resume Builder
- Fill a form to generate a clean PDF Resume
- Download instantly from browser
- No signup, no fuss

---

## ⚙️ Tech Stack

- Python + Flask
- Sentence Transformers (`all-MiniLM-L6-v2`)
- PyMuPDF for PDF extraction
- DOCX parsing via `python-docx`
- Matplotlib (skill comparison pie charts)
- Bootstrap 5 (for styling)

---

## 🗂 Folder Structure

ai-resume-tool/
├── app.py
├── requirements.txt
├── render.yaml
├── uploads/ # User uploaded files
└── templates/
├── index.html # Homepage
├── screener.html # Resume screener UI
└── builder.html # Resume builder form


---

## 🚀 Installation

```bash
git clone https://github.com/soumik2808/ai-resume-tool.git
cd ai-resume-tool

# Setup virtualenv (recommended)
python -m venv virtualenv
.\virtualenv\Scripts\activate      # On Windows
# source virtualenv/bin/activate # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
