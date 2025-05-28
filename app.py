from flask import Flask, render_template, request
import fitz  # PyMuPDF
from keybert import KeyBERT

app = Flask(__name__)
kw_model = KeyBERT()

def extract_text(file_storage):
    text = ""
    with fitz.open(stream=file_storage.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_keywords(text, top_n=10):
    return [kw for kw, _ in kw_model.extract_keywords(text, top_n=top_n)]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    resume_file = request.files['resume']
    jd_file = request.files['jd']

    resume_text = extract_text(resume_file)
    jd_text = extract_text(jd_file)

    resume_keywords = set(extract_keywords(resume_text, top_n=15))
    jd_keywords = set(extract_keywords(jd_text, top_n=15))

    matched = resume_keywords & jd_keywords
    missing = jd_keywords - resume_keywords
    score = int((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0

    return render_template('index.html',
                       score=score,
                       keywords=list(resume_keywords),
                       matched=", ".join(matched),
                       missing=", ".join(missing),
                       resume_text=resume_text,
                       jd_text=jd_text)

if __name__ == '__main__':
    app.run(debug=True)
