
# main.py
from transform.transformator import CsvTransform

if __name__ == "__main__":
    # On lance uniquement la version CSV pour le moment
    csv_transform = CsvTransform()
    df = csv_transform.run()           # Extrait et fusionne toutes les stations
    print(df.head())                   # 👀 Affiche un aperçu dans le terminal
    csv_transform.save_to_csv()        # Sauvegarde ou met à jour le CSV



