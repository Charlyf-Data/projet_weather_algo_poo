import pytest
from projet.extractors.extractor_factory import ExtractorFactory
from projet.extractors.csv_extractor import CSVExtractor
from projet.extractors.api_extractor import ApiExtractor
from projet.extractors.meteo_toulouse_extractor_chainee import MeteoToulouseExtractorChainnee


def test_factory_returns_csv_extractor():
    extractor = ExtractorFactory.get_extractor(
        "csv",
        chemin_fichier="test.csv"
    )
    assert isinstance(extractor, CSVExtractor)


def test_factory_returns_api_extractor():
    extractor = ExtractorFactory.get_extractor(
        "api",
        url="http://test.com",
        params={"a": 1}
    )
    assert isinstance(extractor, ApiExtractor)


def test_factory_returns_meteo_extractor():
    extractor = ExtractorFactory.get_extractor(
        "meteo_toulouse",
        station="montaudran"
    )
    assert isinstance(extractor, MeteoToulouseExtractorChainnee)


def test_factory_missing_csv_argument():
    with pytest.raises(ValueError, match="Missing 'chemin_fichier'"):
        ExtractorFactory.get_extractor("csv")


def test_factory_missing_api_argument():
    with pytest.raises(ValueError, match="Missing 'url'"):
        ExtractorFactory.get_extractor("api")


def test_factory_missing_meteo_argument():
    with pytest.raises(ValueError, match="Missing 'station'"):
        ExtractorFactory.get_extractor("meteo_toulouse")


def test_factory_unknown_type():
    with pytest.raises(ValueError, match="Unknown extractor type"):
        ExtractorFactory.get_extractor("unknown")
