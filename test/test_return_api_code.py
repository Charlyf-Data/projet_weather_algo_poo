import pytest
from projet.extractors.api_extractor import ApiExtractor
from unittest.mock import patch, Mock


def test_api_extractor_extract_success():
    url = "https://example.com/api/data"
    params = {"key": "value"}

    extractor = ApiExtractor(url, params)

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "ok"}

    with patch("projet.extractors.api_extractor.requests.get", return_value=mock_response):
        result = extractor.extract()

    assert result == {"data": "ok"}


def test_api_extractor_extract_failure():
    url = "https://example.com/api/data"
    params = {"key": "value"}

    extractor = ApiExtractor(url, params)

    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    with patch("projet.extractors.api_extractor.requests.get", return_value=mock_response):
        with pytest.raises(Exception) as exc_info:
            extractor.extract()

    assert "Erreur API 500" in str(exc_info.value)
