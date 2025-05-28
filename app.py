from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF for PDF
import docx  # for .docx
from sentence_transformers import SentenceTransformer, util
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample tech-related skills (expand as needed)
tech_skills = [
    "python", "flask", "django", "html", "css", "javascript", "sql", "mysql",
    "postgresql", "aws", "azure", "gcp", "docker", "kubernetes", "git", "linux",
    "nlp", "data analysis", "machine learning", "deep learning", "tensorflow",
    "pytorch", "scikit-learn", "communication", "leadership", "problem solving"
]

# Extract text from .pdf or .docx
def extract_text(file):
    if file.filename.endswith('.pdf'):
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text
    elif file.filename.endswith('.docx'):
        doc = docx.Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

# Clean and normalize text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    resume_file = request.files.get("resume")
    jd_file = request.files.get("jd")

    if not resume_file or not jd_file:
        return "Please upload both Resume and Job Description", 400

    # Extract and clean
    resume_text = clean_text(extract_text(resume_file))
    jd_text = clean_text(extract_text(jd_file))

    # Semantic similarity scores
    embeddings_resume = model.encode([resume_text])[0]
    matched_skills = []
    missing_skills = []

    for skill in tech_skills:
        sim = util.cos_sim(model.encode(skill), embeddings_resume)
        if sim > 0.4:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    jd_matched = []
    jd_missing = []

    embeddings_jd = model.encode([jd_text])[0]
    for skill in tech_skills:
        sim = util.cos_sim(model.encode(skill), embeddings_jd)
        if sim > 0.4:
            jd_matched.append(skill)
        else:
            jd_missing.append(skill)

    score = int((len(matched_skills) / len(tech_skills)) * 100)

    return render_template("index.html",
                           score=score,
                           resume_text=resume_text,
                           jd_text=jd_text,
                           matched=matched_skills,
                           missing=missing_skills,
                           jd_matched=jd_matched,
                           jd_missing=jd_missing
                           )

if __name__ == "__main__":
    app.run(debug=True)
