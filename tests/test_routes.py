def test_screener_post(client):
    data = {
        'resume': (open('tests/sample_resume.pdf', 'rb'), 'sample_resume.pdf'),
        'jd': (open('tests/sample_jd.txt', 'rb'), 'sample_jd.txt')
    }
    response = client.post('/screener', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b"Resume Score" in response.data
