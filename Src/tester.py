# # recupere une donnée de mongodb

# import pymongo

# def get_data_from_mongodb():
#     url = "mongodb+srv://Noa:Griffith@operation-eclipse.cqvrd.mongodb.net/"
#     client = pymongo.MongoClient(url)
#     db = client['test1']
#     collection = db['guts']
#     data = collection.find_one()
#     return data

# data = get_data_from_mongodb()
# print(data['test'])


# fetch data from api https://tabular-api.data.gouv.fr/api/resources/1c5075ec-7ce1-49cb-ab89-94f507812daf/ and whrite the data in a file

import requests
import pandas as pd

def fetch_data_from_api():
    url = "https://tabular-api.data.gouv.fr/api/resources/b8703c69-a18f-46ab-9e7f-3a8368dcb891/data/csv/"
    response = requests.get(url)
    data = response.json()
    return data

def write_data_to_file(data, filename='csv/data.csv'):
    with open(filename, mode='w', encoding='utf-8') as file:
        file.write(data)
        
        
def normalize_data(data):
    data = fetch_data_from_api()
    # replace ' with " in the data and , with ,\n
    data = str(data).replace("'", '"')
    return data
    
        
# def json_to_csv(data):
#     write_data_to_file(data)
#     df = pd.read_json('data.json')
#     df.to_csv('csv/data.csv', index=False)
#     return df
        
        

def main():
    data = normalize_data(fetch_data_from_api())
    write_data_to_file(data)
    # json_to_csv(data)
    
    
if __name__ == '__main__':
    main()
