import pymongo

def connect_to_db():
    """
    Établit la connexion avec MongoDB Atlas et retourne le client.
    """
    try:
        # Connexion à MongoDB Atlas
        client = pymongo.MongoClient(
            "mongodb+srv://Noa:Griffith@operation-eclipse.cqvrd.mongodb.net/?retryWrites=true&w=majority",
            tlsAllowInvalidCertificates=True
        )
        print("Connexion établie avec la base de données.")
        return client
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None


def print_all_data():
    """
    Affiche toutes les données de la collection 'guts' dans la base 'test1'.
    """
    client = connect_to_db()
    if client is None:
        print("Impossible de se connecter à la base de données.")
        return

    try:
        # Accès à la base de données 'test1' et collection 'guts'
        db = client['test1']
        collection = db['guts']

        # Récupération et affichage de tous les documents
        print("Documents trouvés dans la collection 'guts' :")
        for document in collection.find():
            print(document)
    except Exception as e:
        print(f"Erreur lors de la lecture des données : {e}")
    finally:
        # Fermeture de la connexion
        client.close()
        print("Connexion fermée.")


if __name__ == '__main__':
    print_all_data()
