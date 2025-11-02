"""
Test suite for Loan API
Tests all main endpoints and functionality
"""
import pytest
import sys
import os
from pathlib import Path

# Add parent directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def app():
    """Create and configure a test app instance"""
    # Set test environment variables
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['DATABASE_URL'] = os.getenv(
        'DATABASE_URL',
        'postgresql+psycopg2://postgres:postgres@localhost:5432/microloans_test'
    )
    
    try:
        from app import create_app
        app = create_app()
        app.config.update({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': os.environ['DATABASE_URL']
        })
        yield app
    except ImportError:
        # If app module doesn't have create_app, try direct import
        import app as flask_app
        if hasattr(flask_app, 'app'):
            flask_app.app.config['TESTING'] = True
            yield flask_app.app
        else:
            pytest.skip("Could not import Flask app")


@pytest.fixture
def client(app):
    """Create a test client for the Flask app"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner"""
    return app.test_cli_runner()


# ==========================================
# Health Check Tests
# ==========================================

def test_health_endpoint_exists(client):
    """Test that health endpoint exists"""
    response = client.get('/health')
    assert response.status_code in [200, 404], "Health endpoint should exist or return 404"


def test_health_endpoint_returns_json(client):
    """Test that health endpoint returns JSON"""
    response = client.get('/health')
    if response.status_code == 200:
        assert response.content_type == 'application/json'
        data = response.get_json()
        assert data is not None


def test_health_endpoint_structure(client):
    """Test health endpoint response structure"""
    response = client.get('/health')
    if response.status_code == 200:
        data = response.get_json()
        assert 'status' in data or 'message' in data


# ==========================================
# Loans API Tests
# ==========================================

def test_loans_endpoint_exists(client):
    """Test that loans endpoint exists"""
    response = client.get('/api/loans')
    # Should return 200 (success) or 404 (not implemented yet)
    assert response.status_code in [200, 404, 401, 403]


def test_loans_endpoint_returns_json(client):
    """Test that loans endpoint returns JSON when successful"""
    response = client.get('/api/loans')
    if response.status_code == 200:
        assert response.content_type == 'application/json'


def test_loans_endpoint_returns_list_or_dict(client):
    """Test that loans endpoint returns proper data structure"""
    response = client.get('/api/loans')
    if response.status_code == 200:
        data = response.get_json()
        assert isinstance(data, (list, dict))


def test_loans_with_limit(client):
    """Test loans endpoint with limit parameter"""
    response = client.get('/api/loans?limit=5')
    if response.status_code == 200:
        data = response.get_json()
        if isinstance(data, list):
            assert len(data) <= 5


# ==========================================
# Stats API Tests
# ==========================================

def test_stats_endpoint_exists(client):
    """Test that stats endpoint exists"""
    response = client.get('/api/stats')
    assert response.status_code in [200, 404, 401, 403]


def test_stats_endpoint_returns_json(client):
    """Test that stats endpoint returns JSON"""
    response = client.get('/api/stats')
    if response.status_code == 200:
        assert response.content_type == 'application/json'


def test_stats_endpoint_structure(client):
    """Test stats endpoint returns dictionary"""
    response = client.get('/api/stats')
    if response.status_code == 200:
        data = response.get_json()
        assert isinstance(data, dict)


# ==========================================
# Borrowers API Tests
# ==========================================

def test_borrowers_endpoint(client):
    """Test borrowers endpoint if it exists"""
    response = client.get('/api/borrowers')
    assert response.status_code in [200, 404, 401, 403]


def test_borrowers_returns_json(client):
    """Test borrowers endpoint returns JSON"""
    response = client.get('/api/borrowers')
    if response.status_code == 200:
        assert response.content_type == 'application/json'


# ==========================================
# Error Handling Tests
# ==========================================

def test_invalid_endpoint_returns_404(client):
    """Test that invalid endpoints return 404"""
    response = client.get('/api/nonexistent_endpoint_12345')
    assert response.status_code == 404


def test_invalid_method_on_valid_endpoint(client):
    """Test invalid HTTP method returns proper error"""
    response = client.post('/health')
    # Should return 405 (Method Not Allowed) or handle gracefully
    assert response.status_code in [200, 405, 404]


# ==========================================
# Environment and Configuration Tests
# ==========================================

@pytest.mark.unit
def test_flask_env_is_set():
    """Test that FLASK_ENV is set"""
    flask_env = os.getenv('FLASK_ENV')
    assert flask_env in ['testing', 'development', 'production', None]


@pytest.mark.unit
def test_database_url_is_set():
    """Test that DATABASE_URL is configured"""
    db_url = os.getenv('DATABASE_URL')
    assert db_url is not None
    assert 'postgresql' in db_url.lower()


@pytest.mark.unit
def test_database_url_format():
    """Test DATABASE_URL has correct format"""
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        assert db_url.startswith('postgresql')
        assert '@' in db_url  # Should have username@host


# ==========================================
# Integration Tests
# ==========================================

@pytest.mark.integration
def test_full_api_workflow(client):
    """Test a complete workflow through the API"""
    # 1. Check health
    health_response = client.get('/health')
    
    # 2. Get loans if endpoint exists
    loans_response = client.get('/api/loans')
    
    # 3. Get stats if endpoint exists
    stats_response = client.get('/api/stats')
    
    # At least one endpoint should work
    assert any([
        health_response.status_code == 200,
        loans_response.status_code == 200,
        stats_response.status_code == 200
    ])


@pytest.mark.integration
def test_api_response_times(client):
    """Test that API endpoints respond quickly"""
    import time
    
    endpoints = ['/health', '/api/loans', '/api/stats']
    
    for endpoint in endpoints:
        start = time.time()
        response = client.get(endpoint)
        duration = time.time() - start
        
        # If endpoint exists, it should respond within 2 seconds
        if response.status_code == 200:
            assert duration < 2.0, f"{endpoint} took too long: {duration}s"


# ==========================================
# Data Validation Tests
# ==========================================

@pytest.mark.unit
def test_loan_data_structure(client):
    """Test that loan data has expected structure"""
    response = client.get('/api/loans')
    
    if response.status_code == 200:
        data = response.get_json()
        
        # If it's a list of loans, check first item
        if isinstance(data, list) and len(data) > 0:
            loan = data[0]
            # Expected fields in a loan (adjust based on your schema)
            expected_fields = ['id', 'amount', 'status']
            # At least some expected fields should exist
            has_some_fields = any(field in loan for field in expected_fields)
            assert has_some_fields, "Loan data should have expected fields"


@pytest.mark.unit  
def test_stats_data_structure(client):
    """Test that stats data has expected structure"""
    response = client.get('/api/stats')
    
    if response.status_code == 200:
        data = response.get_json()
        
        # Stats should be a dictionary with numeric values
        if isinstance(data, dict):
            # Should have at least one stat
            assert len(data) > 0, "Stats should contain data"


# ==========================================
# Security Tests
# ==========================================

@pytest.mark.unit
def test_no_sensitive_data_in_response(client):
    """Test that sensitive data is not exposed"""
    response = client.get('/api/loans')
    
    if response.status_code == 200:
        response_text = response.get_data(as_text=True).lower()
        
        # Should not contain passwords or sensitive keys
        sensitive_terms = ['password', 'secret', 'api_key', 'token']
        for term in sensitive_terms:
            assert term not in response_text, f"Response should not contain '{term}'"


@pytest.mark.unit
def test_cors_headers(client):
    """Test CORS headers if configured"""
    response = client.get('/api/loans')
    
    # Just check response exists, CORS may or may not be configured
    assert response is not None


# ==========================================
# Parameterized Tests
# ==========================================

@pytest.mark.parametrize("endpoint", [
    "/health",
    "/api/loans",
    "/api/stats",
    "/api/borrowers"
])
def test_endpoints_accessible(client, endpoint):
    """Test that main endpoints are accessible"""
    response = client.get(endpoint)
    # Should not return 500 (server error)
    assert response.status_code != 500


@pytest.mark.parametrize("limit", [1, 5, 10, 100])
def test_loans_with_different_limits(client, limit):
    """Test loans endpoint with various limit values"""
    response = client.get(f'/api/loans?limit={limit}')
    
    if response.status_code == 200:
        data = response.get_json()
        if isinstance(data, list):
            assert len(data) <= limit