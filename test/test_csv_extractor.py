import pandas as pd
from projet.extractors.csv_extractor import CSVExtractor


def test_extract_valid_csv(tmp_path):
    # Création d’un faux fichier CSV temporaire
    file_path = tmp_path / "test.csv"
    file_path.write_text("col1,col2\n1,2\n3,4")

    extractor = CSVExtractor(str(file_path))
    df = extractor.extract()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]
    assert len(df) == 2


def test_extract_file_not_found():
    extractor = CSVExtractor("fichier_inexistant.csv")
    df = extractor.extract()

    assert isinstance(df, pd.DataFrame)
    assert df.empty
