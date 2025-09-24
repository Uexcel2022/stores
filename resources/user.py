import jwt
from flask_smorest import Blueprint, abort
from  flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, get_jwt
from flask_jwt_extended import jwt_required

from db import db
from models import UserModel
from blocked_jwt import BLOCKlIST
from schemas import UserSchema, TokenSchema

blp = Blueprint('users', __name__, description="User Related APIs Operations")

@blp.route('/register')
class UserRegistration(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        username = UserModel.query.filter_by(username=user_data["username"]).first()

        if username:
            abort(409,
                  messages =f"A user with the username `{user_data["username"]}' already exists.")

        user = UserModel(
            username=user_data['username'],
            password=pbkdf2_sha256.hash(user_data['password'])
        )

        try:
            db.session.add(user)
            db.session.commit()
            return {"message": "User created successfully"}, 201

        except SQLAlchemyError as e:
            abort(500, message='something went wrong')

@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200,TokenSchema)
    def post(self,user_data):
        user = UserModel.query.filter_by(username=user_data["username"]).first()
        if not user or not pbkdf2_sha256.verify(user_data["password"], user.password):
            abort(401, messages =f"Invalid credentials.")
        token = create_access_token(identity= str(user.id))
        access_token = TokenSchema()
        access_token.access_token = token
        access_token.token_type = 'bearer'

        return access_token

@blp.route('/logout')
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKlIST.add(jti)
        return {"message": "You have been logged out."}, 200


@blp.route('/users/<int:user_id>')
class UserDetails(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(user_id)

    @blp.response(204, description="When user is deleted successfully")
    @blp.response(404, description="When user not found")
    def delete(self, user_id):
      res =  db.session.query(UserModel).filter(UserModel.id == user_id).delete()
      if res == 0:
          abort(404, message="user not found")
      db.session.commit()
      return {"message": "User not found"}, 204

