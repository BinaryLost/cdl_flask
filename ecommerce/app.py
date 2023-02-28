from flask import Flask
from .routes.views import adminBluePrint

app = Flask(__name__)
app.register_blueprint(adminBluePrint)

if __name__ == '__main__':
    app.run()
