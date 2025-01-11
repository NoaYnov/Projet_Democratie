import requests
import pandas as pd
from io import StringIO
import os
import requests
import unicodedata



def import_json():
    # European_elections()
    Legislative_elections()
    

def Legislative_elections():
    with open('json/Législatives.json', 'r') as file:
        data = file.read()
        data = data.split('\n')
        for line in data:
            if line:
                line = line.split(',')
                code_T1 = line[1].split(':')[1].replace('"','')
                code_T2 = line[2].split(':')[1].replace('"','')
                year = line[0].split(':')[2].replace('"','').split(' ')[2]
                name_T1 = line[1].split(':')[0].replace('"','').replace(' ','_')+"_"+year
                name_T2 = line[2].split(':')[0].replace('"','').replace(' ','_')+"_"+year+""
                # si le fichier csv existe déjà
                if os.path.isfile(f'csv/Législatives/{name_T1}.csv') and os.path.isfile(f'csv/Législatives/{name_T2}.csv'):
                    print(f"Les fichiers {name_T1}.csv et {name_T2}.csv existent déjà.")
                    pass
                if code_T2 == 'Meme Identifiant que le T1':
                    fetch_data_from_api(code_T1,name_T1,"Législatives")
                    
                else :
                    fetch_data_from_api(code_T1,name_T1,"Législatives")
                    fetch_data_from_api(code_T2,name_T2,"Législatives")
                
def European_elections():
    with open('json/Européennes.json', 'r') as file:
        data = file.read()
        data = data.split('\n')
        for line in data:
            if line:
                line = line.split(',')
                code = line[1].split(':')[1].replace('"','')
                name = line[0].split(':')[2].replace('"','')
                if code == 'Vide':
                    pass
                else:
                    fetch_data_from_api(code,name,"Européennes")

def remove_accents_and_special_chars(text):
    # Normalise le texte pour retirer les accents et autres caractères spéciaux
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def fetch_data_from_api(data,name,folder):
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

    
        with open(f'csv/{folder}/{name}.txt', 'w', encoding='utf-8') as file:
            file.write(clean_text)  
        print("Le fichier txt a été enregistré sans accents ni caractères spéciaux.")
        txt_to_csv(name,folder)
        return None  # On ne retourne pas de données ici, car il s'agit d'un fichier txt
    elif 'text/csv' in response.headers.get('Content-Type', ''):
        clean_text = remove_accents_and_special_chars(response.text)
        with open(f'csv/{folder}/{name}.csv', 'w', encoding='utf-8') as file:
            
            file.write(clean_text) 
    # si le fichier est un xlsx
    # elif 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in response.headers.get('Content-Type', ''):
    #     print("La réponse est au format xlsx.")
    #     # On lit le contenu du fichier xlsx
    #     data = pd.read_excel(StringIO(response.content))
    #     data.to_csv(f'csv/{folder}/{name}.csv', index=False)
    #     print("Le fichier xlsx a été converti en csv.")
#   A faire

def txt_to_csv(name,folder):
    # Convertir le fichier txt en csv
    data = pd.read_csv(f'csv/{folder}{name}.txt', sep=';')
    data.to_csv(f'csv/{folder}{name}.csv', index=False)
    print("Le fichier txt a été converti en csv.")
    # delete file
    os.remove(f'csv/{folder}{name}.txt')


def main():
    # for name in all_requests:
    #     # if file exist pass
    #     if os.path.isfile(f'csv/{name}.csv'):
    #         print(f"Le fichier {name}.csv existe déjà.")
    #         pass
    #     else:
    #         fetch_data_from_api(all_requests[name], name)
    import_json()
    
            




if __name__ == '__main__':
    main()


