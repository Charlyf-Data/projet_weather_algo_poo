# tests/test_meteo_extractor.py
from .extractors.meteo_toulouse_extractor import MeteoToulouseExtractor

def test_init_params():
    extractor = MeteoToulouseExtractor()
    assert "toulouse" in extractor.url.lower()
    assert extractor.url.endswith("/records")

    expected_keys = {"select", "where", "order_by", "limit"}
    assert set(extractor.params.keys()) == expected_keys