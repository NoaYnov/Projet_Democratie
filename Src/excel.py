import pandas as pd
import os
import requests

def main():
    Excel_to_json()

def Excel_to_json():
    # ouvre le fichier Excel Doc/LiensElections.xlsx
    xls = pd.ExcelFile('../Doc/LiensElections.xlsx')
    # récupère le nom des feuilles
    sheets = xls.sheet_names
    # pour chaque feuille
    for sheet in sheets:
        # récupère les données
        data = pd.read_excel(xls, sheet)
        # convertit les données en json
        json_data = data.to_json(orient='records')
        # enregistre le fichier json
        with open(f'json/{sheet}.json', 'w') as file:
            file.write(json_data)
    print("Les fichiers json ont été créés avec succès.")
    data_transformation()
    
    
def data_transformation():
    # ouvre tous les fichiers json et retire les \u00e9 et \u00e8, et rajoute un \n à la fin de chaque ligne
    for file in os.listdir('json'):
        with open(f'json/{file}', 'r') as f:
            data = f.read()
            data = data.replace('\\u00e9', 'e').replace('\\u00e8', 'e').replace('},', '},\n').replace('\\u00c9', 'e')
            
        with open(f'json/{file}', 'w') as f:
            f.write(data)
    print("Les données ont été transformées avec succès.")

if __name__ == '__main__':
    main()