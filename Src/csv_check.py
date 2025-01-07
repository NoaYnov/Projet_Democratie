import requests
import pandas as pd
from io import StringIO
import os
import requests
import unicodedata



def import_json():
    # Importe un fichier json et print le contenu
    with open('json/Européennes.json', 'r') as file:
        data = file.read()
        print(data)
    
    

def remove_accents_and_special_chars(text):
    # Normalise le texte pour retirer les accents et autres caractères spéciaux
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def fetch_data_from_api(data,name):
    url = f"https://www.data.gouv.fr/fr/datasets/r/{data}"
    response = requests.get(url)
    
    
    if response.status_code != 200:
        print(f"Erreur {response.status_code}: La requête a échoué.")
        return None

    # Vérifie si la réponse est bien du contenu textuel
    if 'text/plain' in response.headers.get('Content-Type', ''):
        print("La réponse est au format txt.")
        
        # Retirer les accents et les caractères spéciaux
        clean_text = remove_accents_and_special_chars(response.text)

    
        with open(f'csv/{name}.txt', 'w', encoding='utf-8') as file:
            file.write(clean_text)  
        print("Le fichier txt a été enregistré sans accents ni caractères spéciaux.")
        txt_to_csv(name)
        return None  # On ne retourne pas de données ici, car il s'agit d'un fichier txt
    elif 'text/csv' in response.headers.get('Content-Type', ''):
        clean_text = remove_accents_and_special_chars(response.text)
        with open(f'csv/{name}.csv', 'w', encoding='utf-8') as file:
            
            file.write(clean_text) 
        


def txt_to_csv(name):
    # Convertir le fichier txt en csv
    data = pd.read_csv(f'csv/{name}.txt', sep=';')
    data.to_csv(f'csv/{name}.csv', index=False)
    print("Le fichier txt a été converti en csv.")
    # delete file
    os.remove(f'csv/{name}.txt')


def main():
    # for name in all_requests:
    #     # if file exist pass
    #     if os.path.isfile(f'csv/{name}.csv'):
    #         print(f"Le fichier {name}.csv existe déjà.")
    #         pass
    #     else:
    #         fetch_data_from_api(all_requests[name], name)
    
            




if __name__ == '__main__':
    main()


