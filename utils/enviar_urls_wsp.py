import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
NUMERO_DESTINO = "2604319150"

def enviar_urls_whatsapp(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        urls = json.load(file)

    for grupo_archivo, url in urls.items():
        grupo = grupo_archivo.split("_")[0]  # Extrae "grupo1", "grupo2", etc.
        mensaje = f'{grupo} "{url}"'

        payload = {
            "token": WHATSAPP_TOKEN,
            "to": NUMERO_DESTINO,
            "body": mensaje,
        }

        response = requests.post(WHATSAPP_API_URL, data=payload)

        if response.status_code == 200:
            print(f"✅ Mensaje enviado para {grupo}")
        else:
            print(f"❌ Error al enviar mensaje para {grupo}: {response.status_code} - {response.text}")
