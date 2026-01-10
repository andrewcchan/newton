import pytest
from unittest.mock import patch, MagicMock
import numpy as np

def test_app_model_missing(monkeypatch):
    # Mock numpy.load to raise FileNotFoundError
    with patch('numpy.load', side_effect=FileNotFoundError):
        # We need to reload app to trigger the module-level try-except block
        import sys
        if 'app' in sys.modules:
            del sys.modules['app']
        from app import app

        # Create a test client
        client = app.test_client()

        # Test index route
        response = client.get('/')
        assert response.status_code == 200
        assert b'disabled title="AI model not loaded"' in response.data
        assert b'Let the AI Solve' in response.data

        # Test solve route
        response = client.post('/solve', json={'gravity': 9.8})
        assert response.status_code == 400
        assert b'AI feature is currently unavailable' in response.data

def test_app_model_loaded(monkeypatch):
    # Mock numpy.load to return a dummy q_table
    with patch('numpy.load', return_value=np.zeros((10, 10))):
        # We need to reload app to trigger the module-level try-except block
        import sys
        if 'app' in sys.modules:
            del sys.modules['app']
        from app import app

        # Create a test client
        client = app.test_client()

        # Test index route
        response = client.get('/')
        assert response.status_code == 200
        assert b'disabled' not in response.data

        # We don't test solve route success here as it involves agent logic which requires more mocking
