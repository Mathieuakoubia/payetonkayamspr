from fastapi import Header, HTTPException, Depends
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

WEBSHOP_KEY_ENV_VAR = "WEBSHOP_API_KEY"

def verify_webshop_key(
    x_api_key: str = Header(..., description="Clé API Webshop")
):
    expected_key = os.getenv(WEBSHOP_KEY_ENV_VAR)
    if not expected_key:
        raise HTTPException(status_code=500, detail="Clé API Webshop non configurée sur le serveur")

    if x_api_key != expected_key:
        raise HTTPException(status_code=403, detail="Clé API Webshop invalide")

    # Si tout est OK, on continue sans erreur
    return True
