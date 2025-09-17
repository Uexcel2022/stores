
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import  db
from models import StoreModel
from schemas import StoreSchema

blp = (
    Blueprint('store', __name__, description='Store related operations'))

@blp.route('/stores')
class Store(MethodView):

    @blp.response( 200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
            return store
        except SQLAlchemyError as e:
            abort(500, message='An error occurred.')


@blp.route('/stores/<int:store_id>')
class StoreList(MethodView):
    @blp.response( 200, StoreSchema)
    def get(self,store_id):
        return StoreModel.query.get_or_404(store_id)


    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def put(self,store_data, store_id):
        try:
            db.session.query(StoreModel).filter(StoreModel.id == store_id).update(store_data)
            db.session.commit()
            store =  db.session.get(StoreModel,store_id)
            if store is None:
                abort(404, message="The store not found.")
            return store
        except SQLAlchemyError as e:
            abort(500, message="An error occurred.")


    def delete(self,store_id):
        try:
            store = db.session.query(StoreModel).filter(StoreModel.id == store_id).delete()
            db.session.commit()
            if store == 0:
                return {"message": "The store not found!"},404
            return '', 204
        except SQLAlchemyError as e:
            abort(404, message="An error occurred.")