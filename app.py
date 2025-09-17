import uuid

from flask import Flask
from flask_smorest import Api
from resources.store import blp  as store_blueprint
from resources.item import blp as item_blueprint
app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores Rest API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] ="3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(store_blueprint)
api.register_blueprint(item_blueprint)

