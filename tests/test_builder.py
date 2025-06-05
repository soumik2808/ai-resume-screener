import fitz
from unittest import mock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

with mock.patch('sentence_transformers.SentenceTransformer'):
    from app import app


def test_summary_in_pdf(tmp_path):
    client = app.test_client()
    data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '1234567890',
        'summary': 'Skilled engineer with 5 years experience.',
        'skills': 'Python,Flask',
        'experience': 'Lots of coding',
        'education': 'B.Sc CS'
    }
    response = client.post('/builder', data=data)
    assert response.status_code == 200
    pdf_bytes = response.data
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = "".join(page.get_text() for page in doc)
    assert 'Skilled engineer with 5 years experience.' in text
