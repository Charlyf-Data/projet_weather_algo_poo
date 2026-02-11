from .pipeline import PipelineBuilder
from .extractors.meteo_toulouse_extractor import MeteoToulouseExtractorChainnee
from .extractors.stations_liste import ListeStations, Station

def construire_liste_utilisateur() -> ListeStations:
    """
    Affiche les stations disponibles et construit une liste chaînée
    contenant uniquement les stations choisies par l'utilisateur.
    """
    # 1. On récupère les clés des stations depuis la liste chaînée STATIQUE de l'extracteur.
    # Ceci garantit que la configuration est lue via le Singleton une seule fois.
    cles_stations = MeteoToulouseExtractorChainnee.get_noms_stations() # Utilise une méthode de classe

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
    
    # On récupère l'instance Station déjà construite depuis la liste chaînée statique de l'extracteur
    stations_source = MeteoToulouseExtractorChainnee.STATIONS_LISTE

    for idx in indices_choisis:
        cle = cles_stations[idx]
        
        # 💥 CORRECTION : Trouver l'objet Station complet
        # On utilise la méthode de recherche de la liste chaînée statique.
        station_obj = stations_source.trouver_par_cle(cle)
        
        if station_obj:
            liste.ajouter_fin(station_obj)

    return liste


def main():
    # 1. L'utilisateur construit sa propre liste chaînée
    liste_stations = construire_liste_utilisateur()

    print("\nListe chaînée créée avec les stations suivantes :")
    liste_stations.afficher_stations()

    # 2. Pour chaque station de la liste, on utilise la Pipeline via le Builder
    for station in liste_stations:
        print(f"\n--- Traitement pour la station : {station.cle} ---")

        try:
            # Construction de la pipeline via le Builder (utilise la Factory en interne)
            pipeline = (
                PipelineBuilder()
                .with_extractor("meteo_toulouse", station=station.cle)
                # On peut ajouter .with_validator(...) ou .with_saver(...) ici si besoin
                .build()
            )
            
            # Exécution de la pipeline (utilise le Décorateur sur run())
            df = pipeline.run()
            
            print(f"Aperçu des données pour {station.cle} :")
            print(df.head())
            
        except Exception as e:
            print(f"Erreur dans la pipeline pour {station.cle}: {e}")

if __name__ == "__main__":
    main()