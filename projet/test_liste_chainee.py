from .extractors.meteo_toulouse_extractor_chainee import MeteoToulouseExtractorChainnee

# 1) Afficher toutes les stations (via la liste chaînée)
MeteoToulouseExtractorChainnee.afficher_stations()

# 2) Récupérer les noms de stations
print(MeteoToulouseExtractorChainnee.get_noms_stations())

# 3) Créer un extracteur pour une station donnée
extracteur = MeteoToulouseExtractorChainnee("montaudran")
print("Station sélectionnée :", extracteur.station_name)
