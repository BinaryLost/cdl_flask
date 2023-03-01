from .config import AppConfig
from flask import Flask
from .models.db import db
from flask_migrate import Migrate
from .routes.brand import brandBluePrint
from flask_cors import CORS


app = Flask(__name__)

app.config.from_object(AppConfig)

cors = CORS(app)
db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(brandBluePrint)

if __name__ == '__main__':
    app.run()
