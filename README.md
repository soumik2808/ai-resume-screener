# AI Resume Screener

A smart Flask-based web app to compare resumes with job descriptions using **KeyBERT** for keyword extraction and **PyMuPDF** for accurate PDF parsing.

## 🔍 Features

- Upload both Resume PDF and Job Description PDF
- Extracts and displays full text from both files
- Uses KeyBERT to extract top keywords
- Calculates a **Resume Match Score (out of 100)**
- Highlights matched and missing skills

## 🛠 Tech Stack

- Python (Flask)
- PyMuPDF for text extraction
- KeyBERT + Sentence Transformers
- HTML (Jinja2 templating)

## 📦 Installation

```bash
git clone https://github.com/soumik2808/ai-resume-screener.git
cd ai-resume-screener
python -m venv virtualenv
virtualenv\Scripts\activate
pip install -r requirements.txt
python app.py
