import requests
import shutil
import os
import config


def get_nasa_images(api_key=config.api_key, start_date=config.start_date, end_date=config.end_date, count=config.count, thumbs=config.thumbs):

    # URL de base de l'API de la NASA
    base_url = "https://api.nasa.gov"

    # Endpoint pour récupérer les images de la NASA
    endpoint = "/planetary/apod"

    # Paramètres de la requête
    params = {
        "api_key": api_key,
        "start_date": start_date,
        "end_date": end_date,
        "count": count,
        "thumbs": thumbs
    }

    # Créer un dossier pour enregistrer les images s'il n'existe pas
    if not os.path.exists('static'):
        os.makedirs('static')

    # Requête GET pour récupérer les données de l'API
    response = requests.get(base_url + endpoint, params=params)

    # Vérifier le statut de la réponse
    if response.status_code == 200:
        # Convertir la réponse JSON en une liste de dictionnaires Python
        data_list = response.json()

        # Pour chaque élément de la liste de données, récupérer l'URL de l'image
        for data in data_list:
            image_url = data["url"]

            # Télécharger l'image à partir de l'URL
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(f"static/nasa_image_{data['date']}.jpg", "wb") as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
                print(f"Image du {data['date']} téléchargée avec succès!")
            else:
                print(f"Impossible de télécharger l'image du {data['date']}!")
    else:
        print("La requête a échoué avec le code d'erreur", response.status_code)
