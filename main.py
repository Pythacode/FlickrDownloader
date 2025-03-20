print('Initialisation')

import argparse
import requests
from bs4 import BeautifulSoup
import re
import os
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Télécharge les favoris flirk ")
parser.add_argument("url", type=str, help="Url de la page favoris")
args = parser.parse_args()
url = args.url

try:
    print('Téléchargement de la page')
    
    response = requests.get(url)
    response.raise_for_status()
    
    print('Recherche des images')
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    liens = ["https:" + div.get("src") for div in soup.select('div.photo-list-photo-container img')]

    print("Téléchargement des images")
    
    for lien in tqdm(liens) :
        # Télécharger l'image
        id = re.sub(r"https:\/\/live\.staticflickr\.com\/[0-9]*\/", '', lien)
        id = re.sub(r"_[a-z0-9]*_z\.jpg", '', id)

        image_response = requests.get(lien, stream=True)
        image_response.raise_for_status()
        
        file_name = f"img_{id}.jpg"
        f = open(file_name, "wb")
        response = requests.get(lien)
        f.write(response.content)
        f.close()

    print(f"Fin du téléchargement.\nDossier des images : {os.getcwd()}")

except requests.exceptions.RequestException as e:
    exit(f"Erreur lors de la récupération de la page: {e}")