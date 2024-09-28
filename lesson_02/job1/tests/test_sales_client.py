import os
import pytest
from unittest.mock import patch, Mock

from lesson_02.job1.sales_client import SalesClient, NoAuthTokenError


@patch("requests.get")
def test_get_sales_transactions_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "some_data"}
    mock_get.return_value = mock_response

    client = SalesClient(api_url="http://example.com/api", auth_token="test_token")
    result = client.get_sales_transactions(date="2023-01-01")

    assert result == {"data": "some_data"}
    mock_get.assert_called_once_with(
        url="http://example.com/api",
        params={'date': "2023-01-01", 'page': 1},
        headers={'Authorization': "test_token"},
    )


@patch("requests.get")
def test_get_sales_transactions_failure(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    client = SalesClient(api_url="http://example.com/api", auth_token="test_token")
    result = client.get_sales_transactions(date="2023-01-01")

    assert result is None
    mock_get.assert_called_once_with(
        url="http://example.com/api",
        params={'date': "2023-01-01", 'page': 1},
        headers={'Authorization': "test_token"},
    )


@patch.dict(os.environ, {})
def test_get_sales_transactions_no_auth_token():
    client = SalesClient(api_url="http://example.com/api", auth_token=None)

    with pytest.raises(NoAuthTokenError):
        client.get_sales_transactions(date="2023-01-01")


if __name__ == "__main__":
    pytest.main()
