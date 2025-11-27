from extractors.meteo_toulouse_extractor_chainee import MeteoToulouseExtractorChainnee
from extractors.stations_liste import ListeStations, Station
from extractors.stations_config import STATIONS


def construire_liste_utilisateur() -> ListeStations:
    """
    Affiche les stations disponibles et construit une liste chaînée
    contenant uniquement les stations choisies par l'utilisateur.
    """
    # 1. On récupère les clés des stations à partir du dict STATIONS
    cles_stations = list(STATIONS.keys())

    print("Stations disponibles :")
    for i, cle in enumerate(cles_stations, start=1):
        print(f"{i}. {cle}")
    print()

    # 2. L'utilisateur choisit les stations par numéro
    saisie = input(
        "Tape les numéros des stations que tu veux, séparés par des virgules (ex: 1,3,5) : "
    )

    indices_choisis: list[int] = []
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

    # 3. On construit une liste chaînée de stations à partir des choix
    liste = ListeStations()

    for idx in indices_choisis:
        cle = cles_stations[idx]
        sid, ville, nom_station = STATIONS[cle]
        station_obj = Station(cle, sid, ville, nom_station)
        liste.ajouter_fin(station_obj)

    return liste


def main():
    # 1. L'utilisateur construit sa propre liste chaînée
    liste_stations = construire_liste_utilisateur()

    print("\nListe chaînée créée avec les stations suivantes :")
    liste_stations.afficher_stations()

    # 2. Pour chaque station de la liste, on fait un appel API
    for station in liste_stations:
        # station est un objet Station (grâce au __iter__ de ListeChainee)
        print(f"\nRécupération des données pour la station : {station.cle}")

        extracteur = MeteoToulouseExtractorChainnee(station.cle)

        # Nom de méthode selon ton ApiExtractor (à adapter si ce n'est pas get_data)
        data_json = extracteur.get_data()

        df = extracteur.to_dataframe(data_json)
        print(df.head())


if __name__ == "__main__":
    main()
