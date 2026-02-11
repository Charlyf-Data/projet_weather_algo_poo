# projet/test_liste_chainee.py

from .extractors.meteo_toulouse_extractor_chainee import MeteoToulouseExtractorChainnee
from .extractors.stations_liste import ListeStations, Station
from .extractors.stations_config import STATIONS
import pandas as pd


def construire_liste_utilisateur() -> ListeStations:
    cles_stations = list(STATIONS.keys())

    print("Stations disponibles :")
    for i, cle in enumerate(cles_stations, start=1):
        print(f"{i}. {cle}")
    print()

    saisie = input(
        "Tape les numéros des stations que tu veux, séparés par des virgules (ex: 1,3,5) : "
    )

    indices_choisis = []
    for morceau in saisie.split(","):
        morceau = morceau.strip()
        if not morceau:
            continue
        try:
            idx = int(morceau)
        except ValueError:
            print(f"{morceau} n'est pas un nombre, je l'ignore.")
            continue

        if 1 <= idx <= len(cles_stations):
            indices_choisis.append(idx - 1)
        else:
            print(f"{idx} est hors limite, je l'ignore.")

    liste = ListeStations()
    for idx in indices_choisis:
        cle = cles_stations[idx]
        sid, ville, nom_station = STATIONS[cle]
        station_obj = Station(cle, sid, ville, nom_station)
        liste.ajouter_fin(station_obj)

    return liste


def main():
    liste_stations = construire_liste_utilisateur()

    print("\nListe chaînée créée avec les stations suivantes :")
    liste_stations.afficher_stations()

    dfs = []

    for station in liste_stations:
        print(f"\nRécupération des données pour la station : {station.cle}")

        try:
            extracteur = MeteoToulouseExtractorChainnee(station.cle)
            data_json = extracteur.extract()          # méthode définie dans ApiExtractor
            df = extracteur.to_dataframe(data_json)   # adapter JSON -> DataFrame

            if df.empty:
                print(f"🚫 Pas de données pour {station.cle}, je passe.")
                continue

            df["station_name"] = station.cle
            dfs.append(df)

        except Exception as e:
            print(f"⚠️ Erreur pour {station.cle} → ignorée ({e})")
            continue

    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        print("\nDataFrame final :")
        print(df_final.head())
    else:
        print("\nAucune donnée récupérée.")


if __name__ == "__main__":
    main()
