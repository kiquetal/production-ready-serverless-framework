import pytest
from unittest.mock import patch, MagicMock
import os
import json
from bs4 import BeautifulSoup
from lambdas.index import load_restaurants

@pytest.fixture(autouse=True)
def mock_env_variables():
    with patch.dict(os.environ, {
        'API_GATEWAY': 'https://test-api.example.com/dev',
        'AWS_REGION': 'us-east-1',
        'COGNITO_USER_POOL_ID': 'test-pool-id',
        'COGNITO_WEB_CLIENT_ID': 'test-client-id',
        'default_results': '8',
        'search_url': '/restaurants/search',
        'API_PROD_DOMAIN': 'https://prod-api.example.com'  # Add this
    }):
        yield

@patch('lambdas.index.get_restaurants_via_api')
@patch('lambdas.index.return_page')
def test_load_restaurants_html_structure(mock_return_page, mock_get_restaurants):
    # Remove the mock_env_variables parameter - it's already applied

    # Mock template rendering
    mock_template = MagicMock()
    mock_return_page.return_value = mock_template
    mock_template.render.return_value = "<html><body><h1>Restaurants</h1><div id='restaurants'></div></body></html>"

    # Mock API response with more complete data
    mock_get_restaurants.return_value = [
        {
            "name": "Test Restaurant",
            "cuisine": "Test Cuisine",
            "id": "123",
            "address": "123 Test St",
            "rating": 4.5
        }
    ]

    # Call the function
    try:
        response = load_restaurants({}, {})
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error during function execution: {e}")
        response = e
    # Validate response structure
    assert response['statusCode'] == 200
    assert 'body' in response
