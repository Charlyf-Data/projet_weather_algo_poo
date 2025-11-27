
# main.py
from .transform.transformator import CsvTransform

if __name__ == "__main__":

    csv_transform = CsvTransform()
    df = csv_transform.run()           
    print(df.head())                   
    csv_transform.save_to_csv()       



