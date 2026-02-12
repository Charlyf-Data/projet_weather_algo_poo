import pytest
import pandas as pd
from unittest.mock import Mock
from projet.extractors.pipeline import Pipeline, PipelineBuilder


# =========================================================
# 1️⃣ TEST COMPLET - HAPPY PATH
# =========================================================
def test_pipeline_run_full_flow(capsys):

    # --- Extractor ---
    mock_extractor = Mock()
    mock_extractor.extract.return_value = [{"col": 1}, {"col": 2}]
    mock_extractor.to_dataframe.return_value = pd.DataFrame({"col": [1, 2]})

    # --- Validator ---
    mock_validator = Mock()
    mock_validator.__name__ = "MockValidator"
    mock_validator.validate.return_value = None

    # --- Saver ---
    mock_saver = Mock()

    pipeline = Pipeline()
    pipeline.set_extractor(mock_extractor)
    pipeline.set_validator(mock_validator)
    pipeline.set_saver(mock_saver)

    df = pipeline.run()

    # Vérifications retour
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 1)

    # Vérifications appels
    mock_extractor.extract.assert_called_once()
    mock_extractor.to_dataframe.assert_called_once()
    mock_validator.validate.assert_called_once_with(df)
    mock_saver.assert_called_once_with(df)

    # Vérifications logs
    captured = capsys.readouterr()
    assert "[Pipeline] Starting Pipeline..." in captured.out
    assert "Extraction complete" in captured.out
    assert "Validation successful." in captured.out
    assert "Data saved." in captured.out


# =========================================================
# 2️⃣ ERREUR SI PAS D'EXTRACTOR
# =========================================================
def test_pipeline_raises_without_extractor():

    pipeline = Pipeline()

    with pytest.raises(ValueError, match="No extractor set"):
        pipeline.run()


# =========================================================
# 3️⃣ SANS VALIDATOR
# =========================================================
def test_pipeline_without_validator(capsys):

    mock_extractor = Mock()
    mock_extractor.extract.return_value = []
    mock_extractor.to_dataframe.return_value = pd.DataFrame()

    mock_saver = Mock()

    pipeline = Pipeline()
    pipeline.set_extractor(mock_extractor)
    pipeline.set_saver(mock_saver)

    df = pipeline.run()

    assert isinstance(df, pd.DataFrame)

    captured = capsys.readouterr()
    assert "No validator set, skipping validation." in captured.out


# =========================================================
# 4️⃣ SANS SAVER
# =========================================================
def test_pipeline_without_saver(capsys):

    mock_extractor = Mock()
    mock_extractor.extract.return_value = []
    mock_extractor.to_dataframe.return_value = pd.DataFrame()

    mock_validator = Mock()
    mock_validator.__name__ = "MockValidator"
    mock_validator.validate.return_value = None

    pipeline = Pipeline()
    pipeline.set_extractor(mock_extractor)
    pipeline.set_validator(mock_validator)

    df = pipeline.run()

    assert isinstance(df, pd.DataFrame)

    captured = capsys.readouterr()
    assert "No saver set, skipping save." in captured.out


# =========================================================
# 5️⃣ VALIDATOR QUI ÉCHOUE
# =========================================================
def test_pipeline_validation_failure():

    mock_extractor = Mock()
    mock_extractor.extract.return_value = []
    mock_extractor.to_dataframe.return_value = pd.DataFrame()

    mock_validator = Mock()
    mock_validator.__name__ = "FailingValidator"
    mock_validator.validate.side_effect = Exception("Invalid Data")

    pipeline = Pipeline()
    pipeline.set_extractor(mock_extractor)
    pipeline.set_validator(mock_validator)

    with pytest.raises(Exception, match="Invalid Data"):
        pipeline.run()


# =========================================================
# 6️⃣ TEST BUILDER COMPLET
# =========================================================
def test_pipeline_builder(monkeypatch):

    fake_extractor = Mock()

    # Important : chemin exact du module où c'est importé
    monkeypatch.setattr(
        "projet.extractors.pipeline.ExtractorFactory.get_extractor",
        lambda *args, **kwargs: fake_extractor
    )

    mock_validator = Mock()
    mock_validator.__name__ = "MockValidator"

    mock_saver = Mock()

    builder = PipelineBuilder()

    pipeline = (
        builder
        .with_extractor("csv", chemin_fichier="file.csv")
        .with_validator(mock_validator)
        .with_saver(mock_saver)
        .build()
    )

    assert pipeline.extractor is fake_extractor
    assert pipeline.validator is mock_validator
    assert pipeline.saver is mock_saver
