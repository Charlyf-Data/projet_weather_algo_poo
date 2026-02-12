import pytest
import pandas as pd
from projet.extractors.base_extractor import BaseExtractor


# Classe concrète pour tester la classe abstraite
class DummyExtractor(BaseExtractor):
    def extract(self):
        return [{"col1": 1}, {"col1": 2}]


def test_extract_returns_data():
    extractor = DummyExtractor()
    data = extractor.extract()

    assert isinstance(data, list)
    assert data[0]["col1"] == 1


def test_to_dataframe_returns_dataframe():
    extractor = DummyExtractor()
    data = extractor.extract()
    df = extractor.to_dataframe(data)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["col1"]
    assert len(df) == 2

def test_base_extractor_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseExtractor()