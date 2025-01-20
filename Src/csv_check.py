import requests
import pandas as pd
from io import StringIO
import os
import requests
import unicodedata



def import_json():
    # European_elections()
    # Legislative_elections()
    Presidential_elections()
    

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


def Presidential_elections():
    with open('json/Présidentielle.json', 'r') as file:
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
                if os.path.isfile(f'csv/Présidentielle/{name_T1}.csv') and os.path.isfile(f'csv/Présidentielle/{name_T2}.csv'):
                    print(f"Les fichiers {name_T1}.csv et {name_T2}.csv existent déjà.")
                    pass
                if code_T2 == 'Meme Identifiant que le T1':
                    fetch_data_from_api(code_T1,name_T1,"Présidentielle")
                    
                else :
                    fetch_data_from_api(code_T1,name_T1,"Présidentielle")
                    fetch_data_from_api(code_T2,name_T2,"Présidentielle")



def remove_accents_and_special_chars(text):
    # Normalise le texte pour retirer les accents et autres caractères spéciaux
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def fetch_data_from_api(data, name, folder):
    url = f"https://www.data.gouv.fr/fr/datasets/r/{data}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erreur {response.status_code}: La requête a échoué.")
        return None

    # Vérifie le type de contenu de la réponse
    content_type = response.headers.get('Content-Type', '')
    
    if 'text/plain' in content_type:
        print("La réponse est au format txt.")
        clean_text = remove_accents_and_special_chars(response.text)
        os.makedirs(f'csv/{folder}', exist_ok=True)
        with open(f'csv/{folder}/{name}.txt', 'w', encoding='utf-8') as file:
            file.write(clean_text)  
        print("Le fichier txt a été enregistré sans accents ni caractères spéciaux.")
        txt_to_csv(name, folder)
        return None
    
    elif 'text/csv' in content_type:
        print("La réponse est au format csv.")
        clean_text = remove_accents_and_special_chars(response.text)
        os.makedirs(f'csv/{folder}', exist_ok=True)
        with open(f'csv/{folder}/{name}.csv', 'w', encoding='utf-8') as file:
            file.write(clean_text)
        print("Le fichier csv a été enregistré sans accents ni caractères spéciaux.")
        return None

    elif 'application/vnd.ms-excel' in content_type or 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
        print("La réponse est au format Excel.")
        os.makedirs(f'csv/{folder}', exist_ok=True)
        file_extension = 'xls' if 'application/vnd.ms-excel' in content_type else 'xlsx'
        temp_file_path = f'csv/{folder}/{name}.{file_extension}'
        
        # Sauvegarde temporaire du fichier Excel
        with open(temp_file_path, 'wb') as file:
            file.write(response.content)
        print(f"Le fichier Excel brut a été téléchargé : {temp_file_path}")
        
        try:
            # Lecture du fichier Excel
            excel_data = pd.read_excel(temp_file_path, engine='openpyxl' if file_extension == 'xlsx' else 'xlrd')
            
            # Nettoyage des colonnes texte
            for column in excel_data.select_dtypes(include=['object']).columns:
                excel_data[column] = excel_data[column].apply(remove_accents_and_special_chars)
            
            # Sauvegarde en format CSV
            clean_csv_path = f'csv/{folder}/{name}_cleaned.csv'
            excel_data.to_csv(clean_csv_path, index=False, encoding='utf-8')
            print(f"Le fichier Excel nettoyé a été enregistré en tant que CSV : {clean_csv_path}")
        except Exception as e:
            print(f"Erreur lors de la lecture ou du nettoyage du fichier Excel : {e}")
        finally:
            # Suppression du fichier Excel temporaire
            os.remove(temp_file_path)
            print(f"Le fichier Excel temporaire a été supprimé : {temp_file_path}")
    else:
        print("Format de fichier non pris en charge.")
        return None
    url = f"https://www.data.gouv.fr/fr/datasets/r/{data}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erreur {response.status_code}: La requête a échoué.")
        return None

    # Vérifie si la réponse est bien du contenu textuel
    content_type = response.headers.get('Content-Type', '')
    
    if 'text/plain' in content_type:
        print("La réponse est au format txt.")
        clean_text = remove_accents_and_special_chars(response.text)
        os.makedirs(f'csv/{folder}', exist_ok=True)
        with open(f'csv/{folder}/{name}.txt', 'w', encoding='utf-8') as file:
            file.write(clean_text)  
        print("Le fichier txt a été enregistré sans accents ni caractères spéciaux.")
        txt_to_csv(name, folder)
        return None
    
    elif 'text/csv' in content_type:
        print("La réponse est au format csv.")
        clean_text = remove_accents_and_special_chars(response.text)
        os.makedirs(f'csv/{folder}', exist_ok=True)
        with open(f'csv/{folder}/{name}.csv', 'w', encoding='utf-8') as file:
            file.write(clean_text)
        print("Le fichier csv a été enregistré sans accents ni caractères spéciaux.")
        return None

    elif 'application/vnd.ms-excel' in content_type or 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
        print("La réponse est au format Excel.")
        os.makedirs(f'csv/{folder}', exist_ok=True)
        # file_path = f'csv/{folder}/{name}.xlsx' ou f'csv/{folder}/{name}.xls
        file_path = f'csv/{folder}/{name}.xlsx'
        
        
        
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print("Le fichier Excel brut a été téléchargé.")
        
        # Lecture et nettoyage du contenu Excel
        try:
            excel_data = pd.read_excel(file_path, engine='openpyxl')  # Utilise pandas pour lire le fichier
            # Supposons que vous vouliez nettoyer toutes les colonnes texte
            for column in excel_data.select_dtypes(include=['object']).columns:
                excel_data[column] = excel_data[column].apply(remove_accents_and_special_chars)
            
            # Sauvegarder le fichier nettoyé en format CSV
            clean_csv_path = f'csv/{folder}/{name}_cleaned.csv'
            excel_data.to_csv(clean_csv_path, index=False, encoding='utf-8')
            print(f"Le fichier Excel nettoyé a été enregistré en tant que CSV : {clean_csv_path}")
        except Exception as e:
            print(f"Erreur lors de la lecture ou du nettoyage du fichier Excel : {e}")
    else:
        print("Format de fichier non pris en charge.")
        return None
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


