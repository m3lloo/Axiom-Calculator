"""Unit tests for AXIOM CALC"""
from app import app, UNIT_CONVERSIONS
import pytest
import json


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestCalculator:
    """Test calculator endpoint"""

    def test_index(self, client):
        """Test index page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'AXIOM' in response.data

    def test_simple_calculation(self, client):
        """Test basic calculation"""
        response = client.post('/calculate',
                               json={'expression': '2+2'},
                               content_type='application/json'
                               )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '4'

    def test_calculation_with_spaces(self, client):
        """Test calculation with spaces"""
        response = client.post('/calculate',
                               json={'expression': '  5 + 3  '},
                               content_type='application/json'
                               )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '8'

    def test_division_by_zero(self, client):
        """Test division by zero error"""
        response = client.post('/calculate',
                               json={'expression': '1/0'},
                               content_type='application/json'
                               )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_invalid_expression(self, client):
        """Test invalid expression"""
        response = client.post('/calculate',
                               json={'expression': '2 ++'},
                               content_type='application/json'
                               )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_empty_expression(self, client):
        """Test empty expression"""
        response = client.post('/calculate',
                               json={'expression': ''},
                               content_type='application/json'
                               )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_dangerous_pattern_blocked(self, client):
        """Test that dangerous patterns are blocked"""
        response = client.post('/calculate',
                               json={'expression': '__import__'},
                               content_type='application/json'
                               )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_sqrt_function(self, client):
        """Test sqrt function"""
        response = client.post('/calculate',
                               json={'expression': 'sqrt(16)'},
                               content_type='application/json'
                               )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '4'

    def test_power_function(self, client):
        """Test power function"""
        response = client.post('/calculate',
                               json={'expression': '2^8'},
                               content_type='application/json'
                               )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '256'

    def test_sine_function(self, client):
        """Test sine function (0 degrees = 0)"""
        response = client.post('/calculate',
                               json={'expression': 'sin(0)'},
                               content_type='application/json'
                               )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '0'


class TestConverter:
    """Test converter endpoint"""

    def test_km_to_miles(self, client):
        """Test km to miles conversion"""
        response = client.post('/convert',
                               json={'conversion': 'km_to_mi', 'value': 1},
                               content_type='application/json'
                               )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data
        assert 'label' in data
        assert float(data['result']) > 0

    def test_celsius_to_fahrenheit(self, client):
        """Test celsius to fahrenheit conversion"""
        response = client.post('/convert',
                               json={'conversion': 'c_to_f', 'value': 0},
                               content_type='application/json'
                               )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '32'

    def test_unknown_conversion(self, client):
        """Test unknown conversion type"""
        response = client.post('/convert',
                               json={'conversion': 'unknown', 'value': 1},
                               content_type='application/json'
                               )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_invalid_value(self, client):
        """Test invalid value for conversion"""
        response = client.post('/convert',
                               json={'conversion': 'km_to_mi', 'value': 'invalid'},
                               content_type='application/json'
                               )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_missing_conversion_key(self, client):
        """Test missing conversion key"""
        response = client.post('/convert',
                               json={'value': 1},
                               content_type='application/json'
                               )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


class TestErrors:
    """Test error handling"""

    def test_404_not_found(self, client):
        """Test 404 error"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_invalid_json(self, client):
        """Test invalid JSON request"""
        response = client.post('/calculate',
                               data='invalid json',
                               content_type='application/json'
                               )
        assert response.status_code == 400


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
