from ecommerce.app import app
import os
from dotenv import load_dotenv

# Charge les variables d'environnement du fichier .env
load_dotenv()

# Récupère la valeur de FLASK_ENV
flask_env = os.getenv("FLASK_ENV")

if __name__ == '__main__':
    app.run(debug=True)
