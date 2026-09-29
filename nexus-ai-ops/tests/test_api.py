from fastapi.testclient import TestClient
from backend.app.main import app
client=TestClient(app)
def test_health(): assert client.get('/health').json()['status']=='ok'
def test_overview(): assert 'services' in client.get('/api/overview').json()
