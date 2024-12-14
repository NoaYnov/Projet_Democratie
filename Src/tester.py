import requests
import pandas as pd
from io import StringIO
import os
import requests
import unicodedata



# all_requests = disctionary

all_requests = {
    'Pre_2022_T1': '79b5cac4-4957-486b-bbda-322d80868224',
    'Pre_2022_T2': '4dfd05a9-094e-4043-8a19-43b6b6bbe086'
    }




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
        
        # Enregistrer le texte nettoyé dans un fichier .txt
        with open(f'csv/{name}.txt', 'w', encoding='utf-8') as file:
            file.write(clean_text)
            
        print("Le fichier txt a été enregistré sans accents ni caractères spéciaux.")
        return None  # On ne retourne pas de données ici, car il s'agit d'un fichier txt
    return None


def txt_to_csv(name):
    # Convertir le fichier txt en csv
    data = pd.read_csv(f'csv/{name}.txt', sep=';')
    data.to_csv(f'csv/{name}.csv', index=False)
    print("Le fichier txt a été converti en csv.")
    # delete file
    os.remove(f'csv/{name}.txt')


def main():
    for name in all_requests:
        # if file exist pass
        if os.path.isfile(f'csv/{name}.csv'):
            print(f"Le fichier {name}.csv existe déjà.")
            pass
        else:
            fetch_data_from_api(all_requests[name], name)
            txt_to_csv(name)




if __name__ == '__main__':
    main()


