"""
Point d'entrée principal du projet.

Permet à l'utilisateur :
1. De choisir des stations météo disponibles.
2. De construire une liste chaînée personnalisée.
3. D'exécuter une pipeline pour chaque station sélectionnée.
"""

from .extractors.pipeline import PipelineBuilder
from .extractors.meteo_toulouse_extractor_chainee import (
    MeteoToulouseExtractorChainnee,
)
from .extractors.stations_liste import ListeStations


def construire_liste_utilisateur() -> ListeStations:
    """
    Affiche les stations disponibles et construit une liste chaînée
    contenant uniquement les stations choisies par l'utilisateur.
    """
    cles_stations = (
        MeteoToulouseExtractorChainnee.get_noms_stations()
    )

    print("Stations disponibles :")
    for i, cle in enumerate(cles_stations, start=1):
        print(f"{i}. {cle}")
    print()

    saisie = input(
        "Tape les numéros des stations "
        "(ex: 1,3,5) séparés par des virgules : "
    )

    indices_choisis: list[int] = []

    for morceau in saisie.split(","):
        morceau = morceau.strip()
        if not morceau:
            continue

        try:
            idx = int(morceau)
        except ValueError:
            print(f"{morceau} n'est pas un nombre, ignoré.")
            continue

        if 1 <= idx <= len(cles_stations):
            indices_choisis.append(idx - 1)
        else:
            print(f"{idx} est hors limite, ignoré.")

    liste = ListeStations()
    stations_source = MeteoToulouseExtractorChainnee.STATIONS_LISTE

    for idx in indices_choisis:
        cle = cles_stations[idx]
        station_obj = stations_source.trouver_par_cle(cle)

        if station_obj:
            liste.ajouter_fin(station_obj)

    return liste


def main():
    """
    Fonction principale du programme.
    Lance la construction de la liste utilisateur
    puis exécute la pipeline pour chaque station.
    """
    liste_stations = construire_liste_utilisateur()

    print("\nListe chaînée créée avec les stations suivantes :")
    liste_stations.afficher_stations()

    for station in liste_stations:
        print(f"\n--- Traitement pour la station : {station.cle} ---")

        try:
            pipeline = (
                PipelineBuilder()
                .with_extractor(
                    "meteo_toulouse",
                    station=station.cle,
                )
                .build()
            )

            df = pipeline.run()

            print(f"Aperçu des données pour {station.cle} :")
            print(df.head())

        except ValueError as error:
            print(
                f"Erreur de configuration pour {station.cle} : {error}"
            )
        except RuntimeError as error:
            print(
                f"Erreur d'exécution pour {station.cle} : {error}"
            )


if __name__ == "__main__":
    main()
