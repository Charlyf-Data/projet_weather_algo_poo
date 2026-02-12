import pytest
import pandas as pd
from projet.extractors.meteo_toulouse_extractor_chainee import MeteoToulouseExtractorChainnee


# -----------------------------
# 1️⃣ Station inconnue
# -----------------------------
def test_station_inconnue(monkeypatch):
    monkeypatch.setattr(
        MeteoToulouseExtractorChainnee.STATIONS_LISTE,
        "trouver_par_cle",
        lambda x: None
    )

    with pytest.raises(ValueError, match="Station inconnue"):
        MeteoToulouseExtractorChainnee("fake_station")


# -----------------------------
# 2️⃣ Construction correcte
# -----------------------------
def test_initialisation_correcte(monkeypatch):

    class FakeStation:
        cle = "montaudran"
        sid = "12"
        ville = "Toulouse"
        nom_station = "montaudran"

    monkeypatch.setattr(
        MeteoToulouseExtractorChainnee.STATIONS_LISTE,
        "trouver_par_cle",
        lambda x: FakeStation()
    )

    extractor = MeteoToulouseExtractorChainnee("montaudran")

    assert "12-station-meteo-toulouse-montaudran" in extractor.url
    assert extractor.station_name == "montaudran"


# -----------------------------
# 3️⃣ to_dataframe avec results
# -----------------------------
def test_to_dataframe_with_results(monkeypatch):

    class FakeStation:
        cle = "montaudran"
        sid = "12"
        ville = "Toulouse"
        nom_station = "montaudran"

    monkeypatch.setattr(
        MeteoToulouseExtractorChainnee.STATIONS_LISTE,
        "trouver_par_cle",
        lambda x: FakeStation()
    )

    extractor = MeteoToulouseExtractorChainnee("montaudran")

    data_json = {
        "results": [
            {"id": 1, "temperature_en_degre_c": 20},
            {"id": 2, "temperature_en_degre_c": 21}
        ]
    }

    df = extractor.to_dataframe(data_json)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 2


# -----------------------------
# 4️⃣ to_dataframe sans results
# -----------------------------
def test_to_dataframe_without_results(monkeypatch, capsys):

    class FakeStation:
        cle = "montaudran"
        sid = "12"
        ville = "Toulouse"
        nom_station = "montaudran"

    monkeypatch.setattr(
        MeteoToulouseExtractorChainnee.STATIONS_LISTE,
        "trouver_par_cle",
        lambda x: FakeStation()
    )

    extractor = MeteoToulouseExtractorChainnee("montaudran")

    df = extractor.to_dataframe({"bad_key": []})

    captured = capsys.readouterr()

    assert df.empty
    assert "'results' key missing" in captured.out

