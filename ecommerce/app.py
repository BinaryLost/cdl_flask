from .config import AppConfig
from flask import Flask
from .models.db import db
from flask_migrate import Migrate
from .routes.brand import brandBluePrint
from .routes.category import categoryBluePrint
from flask_cors import CORS
from ecommerce.errors import not_found, internal_server_error, bad_request

app = Flask(__name__)

app.config.from_object(AppConfig)

cors = CORS(app)
db.init_app(app)

migrate = Migrate(app, db)
app.register_error_handler(404, not_found)
app.register_error_handler(400, bad_request)
app.register_error_handler(500, internal_server_error)


app.register_blueprint(brandBluePrint)
app.register_blueprint(categoryBluePrint)

if __name__ == '__main__':
    app.run()
