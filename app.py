from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from sentence_transformers import SentenceTransformer
from docx import Document
import fitz  # PyMuPDF
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from fpdf import FPDF
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_keywords(text):
    words = text.lower().split()
    keywords = set([word.strip('.,()[]{}:;"\'') for word in words if len(word) > 2 and word.isalpha()])
    return list(keywords)

def generate_pie_chart(data, title):
    labels = list(data.keys())
    sizes = list(data.values())
    colors = ['green', 'red', 'orange']
    plt.figure(figsize=(4, 4))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title(title)
    plt.axis('equal')
    filename = f"{uuid.uuid4().hex}.png"
    chart_path = os.path.join("static", filename)
    plt.savefig(chart_path)
    plt.close()
    return filename

def generate_report_pdf(score, matched, missing, resume_text, jd_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Resume Match Score: {score}/100", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Matched Keywords:", ln=True)
    for skill in matched:
        pdf.cell(200, 10, txt=f"[MATCHED] {skill}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Missing Keywords:", ln=True)
    for skill in missing:
        pdf.cell(200, 10, txt=f"[MISSING] {skill}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Resume Text:", ln=True)
    for line in resume_text.split('\n'):
        pdf.cell(200, 10, txt=line[:100], ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Job Description Text:", ln=True)
    for line in jd_text.split('\n'):
        pdf.cell(200, 10, txt=line[:100], ln=True)

    filename = f"{uuid.uuid4().hex}.pdf"
    path = os.path.join("static", filename)
    pdf.output(path)
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/screener', methods=['GET', 'POST'])
def screener():
    if request.method == 'POST':
        resume = request.files['resume']
        jd = request.files['jd']

        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(resume.filename))
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(jd.filename))
        resume.save(resume_path)
        jd.save(jd_path)

        if resume.filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_path)
        else:
            resume_text = extract_text_from_docx(resume_path)

        if jd.filename.endswith('.pdf'):
            jd_text = extract_text_from_pdf(jd_path)
        else:
            jd_text = extract_text_from_docx(jd_path)

        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(jd_text)

        matched_resume = [word for word in resume_keywords if word in jd_keywords]
        matched_jd = [word for word in jd_keywords if word in resume_keywords]
        missing_resume = [word for word in jd_keywords if word not in resume_keywords]

        resume_score = int(len(matched_resume) / len(jd_keywords) * 100) if len(jd_keywords) else 0

        chart1 = generate_pie_chart({
            'Matched': len(matched_resume),
            'Missing': len(missing_resume),
            'Total': len(jd_keywords)
        }, 'Resume Skill Match')

        chart2 = generate_pie_chart({
            'Matched': len(matched_jd),
            'Missing': len([k for k in resume_keywords if k not in jd_keywords]),
            'Total': len(resume_keywords)
        }, 'JD Skill Match')

        report_filename = generate_report_pdf(resume_score, matched_resume, missing_resume, resume_text, jd_text)

        return render_template('screener.html',
                               resume_score=resume_score,
                               resume_keywords=resume_keywords,
                               jd_keywords=jd_keywords,
                               matched_resume=matched_resume,
                               chart1=chart1,
                               chart2=chart2,
                               report_filename=report_filename,
                               resume_text=resume_text,
                               jd_text=jd_text)
    return render_template('screener.html')

if __name__ == "__main__":
    app.run(debug=True)
