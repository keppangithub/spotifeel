import pytest
import json
from main import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestErrorHandlers:
    """Tests for error handler functions"""
    
    def test_not_found_handler(self, client):
        """Test 404 error handler"""
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404


class TestAppExists:
    """Basic tests to ensure the app is configured"""
    
    def test_app_exists(self):
        """Test that Flask app exists"""
        assert app is not None
        
    def test_app_is_testing(self, client):
        """Test that app is in testing mode"""
        assert app.config['TESTING'] == True
