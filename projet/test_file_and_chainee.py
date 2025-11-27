# projet/test_file.py

import pandas as pd

from .structure.liste_file import FileFIFO
from .extractors.stations_config import STATIONS
from .extractors.stations_liste import Station,ListeStations
from .extractors.meteo_toulouse_extractor_chainee import MeteoToulouseExtractorChainnee
import time







def construire_liste_stations() -> ListeStations:
    """
    Construit une liste chaînée de Station à partir de STATIONS.
    Sert juste de structure de base (pas de FIFO ici).
    """
    liste = ListeStations()
    liste.charger_depuis_config(STATIONS)
    return liste


def demander_stations_utilisateur(liste_stations: ListeStations) -> list[Station]:
    """
    Affiche les stations depuis la liste chaînée
    et renvoie une liste d'objets Station sélectionnés par l'utilisateur.
    """
    # On transforme la liste chaînée en liste Python pour pouvoir indexer
    stations_python: list[Station] = []
    curseur = liste_stations.premier
    while curseur:
        stations_python.append(curseur.valeur)
        curseur = curseur.prochain

    print("Stations disponibles :")
    for i, station in enumerate(stations_python, start=1):
        print(f"{i}. {station.cle} -> {station.ville} / {station.nom_station}")
    print()

    saisie = input(
        "Tape les numéros des stations que tu veux, séparés par des virgules (ex: 1,3,5) : "
    )

    stations_choisies: list[Station] = []

    for morceau in saisie.split(","):
        morceau = morceau.strip()
        if not morceau:
            continue
        try:
            idx = int(morceau)
        except ValueError:
            print(f"{morceau} n'est pas un nombre, je l'ignore.")
            continue

        if 1 <= idx <= len(stations_python):
            stations_choisies.append(stations_python[idx - 1])
        else:
            print(f"{idx} est hors limite, je l'ignore.")

    return stations_choisies


def construire_file_fifo(stations_choisies: list[Station]) -> FileFIFO:
    """
    Remplit une FileFIFO avec les stations choisies (dans l'ordre donné).
    """
    file = FileFIFO()
    for station in stations_choisies:
        file.ajouter(station)
    return file


def main():
    # 1. Liste chaînée de toutes les stations (structure "logique")
    liste_stations = construire_liste_stations()

    # 2. L'utilisateur choisit certaines stations à partir de la liste chaînée
    stations_choisies = demander_stations_utilisateur(liste_stations)

    if not stations_choisies:
        print("Aucune station choisie, j'arrête.")
        return

    # 3. On met ces stations dans une FILE FIFO
    file_stations = construire_file_fifo(stations_choisies)

    print("\nFile d'attente initiale (FIFO) :")
    file_stations.afficher()

    dfs = []

    # 4. On vide la file : une station toutes les 1 seconde
    while not file_stations.est_vide():
        station = file_stations.retirer()
        print(f"\n⏳ Traitement de la station : {station.cle} ...")
        print("   (attente 1 seconde pour simuler une file d'attente)")
        time.sleep(1)

        try:
            extracteur = MeteoToulouseExtractorChainnee(station.cle)
            data_json = extracteur.extract()
            df = extracteur.to_dataframe(data_json)

            if df.empty:
                print(f"🚫 Pas de données pour {station.cle}, je passe.")
                continue

            df["station_name"] = station.cle
            dfs.append(df)
            print(f"✅ Données récupérées pour {station.cle} ({len(df)} lignes)")

        except Exception as e:
            print(f"⚠️ Erreur pour {station.cle} → ignorée ({e})")
            continue

    # 5. DataFrame final
    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        print("\n📊 DataFrame final (head) :")
        print(df_final.head())
    else:
        print("\n🚫 Aucune donnée récupérée.")


if __name__ == "__main__":
    main()
