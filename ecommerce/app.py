from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config, ProductionConfig, DevelopmentConfig
from .models.db import db
from .routes.brand import brandBluePrint
from .routes.category import categoryBluePrint
from .routes.product import productBluePrint
from ecommerce.errors import not_found, internal_server_error, bad_request, limit_error
import os


app = Flask(__name__)
migrate = Migrate(app, db)

if os.environ.get('FLASK_ENV') == 'production':
    envConfig = ProductionConfig
else:
    envConfig = DevelopmentConfig

app.config.from_object(envConfig)

CORS(app, resources={r"/*": {"origins": envConfig.CORS_ORIGINS}},
     supports_credentials=envConfig.CORS_SUPPORTS_CREDENTIALS,
     allow_headers=envConfig.CORS_HEADERS)

db.init_app(app)

app.register_error_handler(404, not_found)
app.register_error_handler(400, bad_request)
app.register_error_handler(500, internal_server_error)
app.register_error_handler(413, limit_error)

app.register_blueprint(brandBluePrint)
app.register_blueprint(categoryBluePrint)
app.register_blueprint(productBluePrint)

if __name__ == '__main__':
    app.run()
