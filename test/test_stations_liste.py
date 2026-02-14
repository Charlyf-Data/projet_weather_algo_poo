import pytest
from projet.extractors.stations_liste import Station, ListeStations


# =========================================================
# 1️ Test création Station
# =========================================================
def test_station_creation_and_repr():

    station = Station("montaudran", "12", "Toulouse", "montaudran")

    assert station.cle == "montaudran"
    assert station.sid == "12"
    assert station.ville == "Toulouse"
    assert station.nom_station == "montaudran"

    # Test __repr__
    assert "montaudran" in repr(station)
    assert "Toulouse" in repr(station)


# =========================================================
# 2️ Test chargement depuis config
# =========================================================
def test_charger_depuis_config():

    config = {
        "montaudran": ("12", "Toulouse", "montaudran"),
        "marengo": ("2", "Toulouse", "marengo"),
    }

    liste = ListeStations()
    liste.charger_depuis_config(config)

    # Vérifie que les stations sont bien ajoutées
    station1 = liste.trouver_par_cle("montaudran")
    station2 = liste.trouver_par_cle("marengo")

    assert station1 is not None
    assert station2 is not None

    assert station1.sid == "12"
    assert station2.sid == "2"


# =========================================================
# 3️ Test trouver_par_cle trouvé
# =========================================================
def test_trouver_par_cle_found():

    config = {
        "montaudran": ("12", "Toulouse", "montaudran"),
    }

    liste = ListeStations()
    liste.charger_depuis_config(config)

    station = liste.trouver_par_cle("montaudran")

    assert station is not None
    assert station.cle == "montaudran"


# =========================================================
# 4️ Test trouver_par_cle non trouvé
# =========================================================
def test_trouver_par_cle_not_found():

    config = {
        "montaudran": ("12", "Toulouse", "montaudran"),
    }

    liste = ListeStations()
    liste.charger_depuis_config(config)

    station = liste.trouver_par_cle("inconnue")

    assert station is None


# =========================================================
# 5️ Test afficher_stations
# =========================================================
def test_afficher_stations(capsys):

    config = {
        "montaudran": ("12", "Toulouse", "montaudran"),
    }

    liste = ListeStations()
    liste.charger_depuis_config(config)

    liste.afficher_stations()

    captured = capsys.readouterr()

    assert "montaudran -> Toulouse - montaudran (sid=12)" in captured.out
