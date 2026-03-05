import pytest
from app import app  # Adjust based on your app's structure

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_detalle_yogui_success(client):
    # Assuming detalle_yogui is a route in your app that returns a success response.
    response = client.get('/detalle_yogui?param=value')
    assert response.status_code == 200
    assert 'expected_output' in response.get_data(as_text=True)


def test_detalle_yogui_failure(client):
    # Test case for failure scenarios.
    response = client.get('/detalle_yogui?param=invalid_value')
    assert response.status_code == 400
    assert 'error_message' in response.get_data(as_text=True)


def test_detalle_yogui_edge_case(client):
    # Test case for edge cases, e.g., empty parameters.
    response = client.get('/detalle_yogui?param=')
    assert response.status_code == 400
    assert 'error_message_empty' in response.get_data(as_text=True)  
