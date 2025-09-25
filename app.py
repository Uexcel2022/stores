import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.store import blp  as store_blueprint
from resources.item import blp as item_blueprint
from resources.tag import blp as tag_blueprint
from resources.user import blp as user_blueprint
from blocked_jwt import BLOCKlIST
from flask_migrate import Migrate


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores Rest API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] ="3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config['JWT_SECRET_KEY'] = "323226110414990525823922147444992522433"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def revoked_jwt_loader(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKlIST

    @jwt.revoked_token_loader
    def revoked_jwt_response(jwt_header, jwt_payload):
        return jsonify({
            "description": "The token has been revoked.", "error": "token_revoked."
        }
    ),401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({
            "description": "Request token is missing.",
            "error": "Authorization required",
        }
    )),401

    @jwt.invalid_token_loader
    def invalid_token_callback(jwn_header, jwt_payload):
        return (jsonify({
            "description": "The access token signature verification failed.",
            "error": "Invalid token",
        })),401

    @jwt.needs_fresh_token_loader
    def fresh_token_loader(jwt_header, jwt_payload):
        return jsonify({
            "description": "The token is not fresh token.",
            "error": "Fresh token is required.",
        }),401

    @jwt.expired_token_loader
    def expired_token_callback(error,r):
        return (jsonify({
            "description": "The Token has expired",
            "error": "Token_expired",
        })),401

    # @app.before_request
    # def before_request():     //commented because we now use flask migrate to create db
    #     db.create_all()

    api.register_blueprint(store_blueprint)
    api.register_blueprint(item_blueprint)
    api.register_blueprint(tag_blueprint)
    api.register_blueprint(user_blueprint)

    return app




