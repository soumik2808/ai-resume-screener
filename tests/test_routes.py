def test_screener_get(client):
    resp = client.get('/screener')
    assert resp.status_code == 200
    assert b'Resume Screener' in resp.data
    assert b'Upload Resume' in resp.data

def test_builder_get(client):
    resp = client.get('/builder')
    assert resp.status_code == 200
    assert b'Resume Builder' in resp.data
    assert b'Full Name' in resp.data
