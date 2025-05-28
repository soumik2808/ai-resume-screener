from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import PyPDF2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    text = ""
    if request.method == "POST":
        resume = request.files.get("resume")
        if resume:
            filename = secure_filename(resume.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume.save(filepath)

            if filename.endswith(".pdf"):
                with open(filepath, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    text = "\n".join([page.extract_text() or "" for page in reader.pages])
            else:
                text = "Only PDF parsing is currently supported."

            message = f"Resume uploaded successfully: {filename}"

    return render_template("index.html", message=message, text=text)

if __name__ == "__main__":
    app.run(debug=True)
